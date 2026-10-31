"""Local-only HTTP operations lab. This is not an internet-facing production server.

Workflow effects may commit before a deadline/disconnect: inspect persisted state
before retry. Each operation owns its SQLite connections in a spawned process.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import multiprocessing as mp
import os
from pathlib import Path
import re
import select
import signal
import socket
import sqlite3
import sys
import threading
import time
import uuid

from langchain_learning.rag import ModelOutputError
from langchain_learning.runtime import load_environment, state_dir

IDENTIFIER = re.compile(r"[A-Za-z0-9_-]{1,80}\Z")
MAX_BODY = 16_384


class RequestFailure(Exception):
    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def event(name: str, **fields) -> None:
    # Never log headers, prompts, drafts, bearer tokens or provider exception text.
    print(json.dumps({"event": name, **fields}), file=sys.stderr, flush=True)


def workflow_worker(sender, db: str, actions: str, user: str, operation: str, body: dict) -> None:
    from langchain_learning.workflow import SupportWorkflow
    try:
        with SupportWorkflow(Path(db), Path(actions)) as workflow:
            if operation == "start":
                value = workflow.start(user, body["thread_id"], body["question"],
                                       draft=body.get("draft"), live=body.get("live", False))
            elif operation == "inspect":
                value = workflow.inspect(user, body["thread_id"])
            elif operation == "decision":
                value = workflow.decide(user, body["thread_id"], body["decision"],
                                        edited_draft=body.get("edited_draft"))
            elif operation == "actions":
                value = workflow.actions(user)
            else:
                raise ValueError("Unknown operation")
        sender.send((200, {"result": value}))
    except PermissionError as exc:
        sender.send((403, {"error": "forbidden", "error_type": type(exc).__name__}))
    except ModelOutputError as exc:
        event("workflow_failed", error_type=type(exc).__name__)
        sender.send((502, {"error": "workflow_or_upstream_failure", "error_type": type(exc).__name__}))
    except ValueError as exc:
        sender.send((400, {"error": "invalid_request_or_state", "error_type": type(exc).__name__}))
    except Exception as exc:
        # Explicit failure visibility without exposing upstream URLs, credentials or document text.
        event("workflow_failed", error_type=type(exc).__name__)
        sender.send((502, {"error": "workflow_or_upstream_failure", "error_type": type(exc).__name__}))
    finally:
        sender.close()


class LocalWorkflowServer(ThreadingHTTPServer):
    daemon_threads = False
    block_on_close = True
    allow_reuse_address = True
    request_queue_size = 16

    def __init__(self, address, *, tokens: dict, db: Path, actions: Path,
                 deadline: float = 30, max_workers: int = 4):
        if address[0] != "127.0.0.1":
            raise ValueError("Course server only binds 127.0.0.1")
        if not 0.1 <= deadline <= 60 or not 1 <= max_workers <= 16:
            raise ValueError("Deadline must be 0.1..60 seconds and workers 1..16")
        self.tokens, self.db, self.actions = tokens, db, actions
        self.deadline = deadline
        self.slots = threading.BoundedSemaphore(max_workers)
        self.stopping = threading.Event()
        self.records: OrderedDict[str, dict] = OrderedDict()
        self.records_lock = threading.Lock()
        self.context = mp.get_context("spawn")
        super().__init__(address, WorkflowHandler)

    def process_request(self, request, client_address):
        if self.stopping.is_set() or not self.slots.acquire(blocking=False):
            try:
                request.settimeout(0.2)
                request.sendall(b'HTTP/1.0 503 Service Unavailable\r\nContent-Length: 22\r\nConnection: close\r\nRetry-After: 1\r\n\r\n{"error":"overloaded"}')
            except OSError as exc:
                event("overload_client_disconnected", error_type=type(exc).__name__)
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def record(self, request_id: str, user: str, status: str, **fields) -> None:
        with self.records_lock:
            self.records[request_id] = {"request_id": request_id, "user_id": user,
                                        "status": status, **fields}
            self.records.move_to_end(request_id)
            while len(self.records) > 256:
                self.records.popitem(last=False)
        event(status, request_id=request_id, **fields)


class WorkflowHandler(BaseHTTPRequestHandler):
    server: LocalWorkflowServer
    server_version = "CourseLocalHTTP"
    sys_version = ""

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(min(self.server.deadline, 5))
        self.started = time.monotonic()

    def log_message(self, format, *args) -> None:
        # Replace default raw request-line logging (query strings can contain secrets).
        event("http_response", method=getattr(self, "command", "unknown"))

    def send_json(self, status: int, value: dict) -> None:
        payload = json.dumps(value, ensure_ascii=True).encode()
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            if hasattr(self, "request_id"):
                self.send_header("X-Request-ID", self.request_id)
            self.end_headers()
            self.wfile.write(payload)
            self.wfile.flush()
        except OSError as exc:
            event("response_disconnected", request_id=getattr(self, "request_id", None),
                  error_type=type(exc).__name__, effects="Inspect persisted thread; commits may already exist")
            if hasattr(self, "user") and hasattr(self, "request_id"):
                self.server.record(self.request_id, self.user, "response_disconnected",
                                   effects_may_have_committed=True)
        self.close_connection = True

    def authenticate(self) -> str:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            raise RequestFailure(401, "bearer_required")
        candidate = header[7:]
        for token, user in self.server.tokens.items():
            if hmac.compare_digest(candidate.encode(), token.encode()):
                return user
        raise RequestFailure(401, "invalid_bearer")

    def read_body(self, allowed: set[str]) -> dict:
        if self.headers.get("Transfer-Encoding"):
            raise RequestFailure(400, "transfer_encoding_unsupported")
        if self.headers.get_content_type() != "application/json":
            raise RequestFailure(415, "json_required")
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            raise RequestFailure(400, "invalid_content_length") from None
        if not 0 <= length <= MAX_BODY:
            raise RequestFailure(413, "body_size_limit")
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise RequestFailure(400, "incomplete_body")
            body = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise RequestFailure(400, "invalid_json") from None
        if not isinstance(body, dict) or set(body) - allowed:
            raise RequestFailure(400, "unexpected_fields_identity_is_token_bound")
        return body

    def validate_text(self, body: dict, key: str, *, optional: bool = False) -> None:
        if optional and key not in body:
            return
        value = body.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > 8_000:
            raise RequestFailure(400, "invalid_" + key)

    def disconnected(self) -> bool:
        readable, _, _ = select.select([self.connection], [], [], 0)
        if readable:
            try:
                return self.connection.recv(1, socket.MSG_PEEK) == b""
            except (ConnectionResetError, BrokenPipeError):
                return True
        return False

    def invoke(self, operation: str, body: dict) -> tuple[int, dict]:
        with self.server.records_lock:
            if self.request_id in self.server.records:
                raise RequestFailure(409, "request_id_already_used")
            self.server.records[self.request_id] = {"request_id": self.request_id,
                "user_id": self.user, "status": "running"}
        self.server.record(self.request_id, self.user, "running")
        receiver, sender = self.server.context.Pipe(duplex=False)
        process = self.server.context.Process(target=workflow_worker,
            args=(sender, str(self.server.db), str(self.server.actions), self.user, operation, body))
        process.start()
        sender.close()
        try:
            while True:
                if self.server.stopping.is_set():
                    self.server.record(self.request_id, self.user, "server_stopping", effects_may_have_committed=True)
                    raise RequestFailure(503, "server_stopping_inspect_thread")
                if self.disconnected():
                    self.server.record(self.request_id, self.user, "cancelled", effects_may_have_committed=True)
                    raise RequestFailure(499, "client_disconnected_inspect_thread")
                if time.monotonic() - self.started >= self.server.deadline:
                    self.server.record(self.request_id, self.user, "deadline_exceeded", effects_may_have_committed=True)
                    raise RequestFailure(504, "deadline_exceeded_inspect_thread")
                if receiver.poll(0.05):
                    try:
                        status, value = receiver.recv()
                    except EOFError:
                        raise RequestFailure(502, "worker_exited_without_result") from None
                    self.server.record(self.request_id, self.user, "completed" if status == 200 else "failed",
                                       http_status=status, elapsed_seconds=time.monotonic() - self.started,
                                       error_type=value.get("error_type"))
                    return status, {**value, "request_id": self.request_id}
                if not process.is_alive():
                    raise RequestFailure(502, "worker_exited_without_result")
        finally:
            if process.is_alive():
                process.terminate()
            process.join(timeout=1)
            if process.is_alive():
                process.kill()
                process.join()
            receiver.close()
            process.close()

    def route(self) -> None:
        if self.path == "/health" and self.command == "GET":
            self.send_json(200, {"status": "alive", "local_only": True})
            return
        if self.path == "/ready" and self.command == "GET":
            try:
                for path in (self.server.db, self.server.actions):
                    with sqlite3.connect(f"file:{path}?mode=rw", uri=True, timeout=0.2) as conn:
                        conn.execute("SELECT 1").fetchone()
                ready = not self.server.stopping.is_set()
            except sqlite3.Error as exc:
                event("readiness_failed", error_type=type(exc).__name__)
                ready = False
            self.send_json(200 if ready else 503, {"ready": ready, "model_provider_probed": False})
            return
        self.user = self.authenticate()
        supplied_id = self.headers.get("X-Request-ID", uuid.uuid4().hex)
        if not IDENTIFIER.fullmatch(supplied_id):
            raise RequestFailure(400, "invalid_request_id")
        self.request_id = supplied_id
        with self.server.records_lock:
            if self.request_id in self.server.records:
                raise RequestFailure(409, "request_id_already_used")
        if self.command == "GET" and self.path.startswith("/requests/"):
            key = self.path.removeprefix("/requests/")
            with self.server.records_lock:
                result = self.server.records.get(key)
                if result is None or result["user_id"] != self.user:
                    raise RequestFailure(404, "request_not_found")
                result = dict(result)
            self.send_json(200, {"result": result, "transient": True})
            return
        if self.command == "GET" and self.path == "/actions":
            status, value = self.invoke("actions", {})
        elif self.command == "POST" and self.path == "/threads/start":
            body = self.read_body({"thread_id", "question", "draft", "live"})
            if not isinstance(body.get("thread_id"), str) or not IDENTIFIER.fullmatch(body["thread_id"]):
                raise RequestFailure(400, "invalid_thread_id")
            self.validate_text(body, "question")
            self.validate_text(body, "draft", optional=True)
            if "live" in body and not isinstance(body["live"], bool):
                raise RequestFailure(400, "live_must_be_boolean")
            if "draft" not in body and not body.get("live", False):
                raise RequestFailure(400, "human_draft_or_explicit_live_required")
            status, value = self.invoke("start", body)
        else:
            match = re.fullmatch(r"/threads/([A-Za-z0-9_-]{1,80})(/decision)?", self.path)
            if not match:
                raise RequestFailure(404, "route_not_found")
            thread_id, decision_suffix = match.groups()
            if self.command == "GET" and not decision_suffix:
                status, value = self.invoke("inspect", {"thread_id": thread_id})
            elif self.command == "POST" and decision_suffix:
                body = self.read_body({"decision", "edited_draft"})
                if not isinstance(body.get("decision"), str) or body["decision"] not in {"approve", "reject", "edit"}:
                    raise RequestFailure(400, "invalid_decision")
                self.validate_text(body, "edited_draft", optional=body["decision"] != "edit")
                status, value = self.invoke("decision", {**body, "thread_id": thread_id})
            else:
                raise RequestFailure(405, "method_not_allowed")
        self.send_json(status, value)

    def dispatch(self) -> None:
        try:
            self.route()
        except RequestFailure as exc:
            self.send_json(exc.status, {"error": exc.code})
        except (TimeoutError, socket.timeout):
            event("request_read_timeout")
            self.send_json(408, {"error": "request_read_timeout"})
        except Exception as exc:
            event("request_failed", error_type=type(exc).__name__)
            self.send_json(500, {"error": "internal_failure", "error_type": type(exc).__name__})

    do_GET = dispatch
    do_POST = dispatch


def auth_tokens() -> dict[str, str]:
    try:
        tokens = json.loads(os.environ.get("COURSE_AUTH_TOKENS", ""))
    except json.JSONDecodeError:
        raise ValueError("Set COURSE_AUTH_TOKENS to a JSON object mapping bearer tokens to identities") from None
    if (not isinstance(tokens, dict) or not tokens or
        any(not isinstance(token, str) or len(token) < 16 or not token.isascii() or
            any(char.isspace() for char in token) or not isinstance(user, str) or
            user not in {"alice", "bob", "finance"}
            for token, user in tokens.items())):
        raise ValueError("Auth tokens require 16+ ASCII non-whitespace characters and known identities")
    return tokens


def main() -> None:
    load_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--deadline", type=float, default=30)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--db", type=Path)
    parser.add_argument("--actions", type=Path)
    args = parser.parse_args()
    tokens = auth_tokens()
    root = state_dir() / "service"
    root.mkdir(parents=True, exist_ok=True)
    db, actions = args.db or root / "checkpoints.sqlite", args.actions or root / "actions.sqlite"
    from langchain_learning.workflow import SupportWorkflow
    with SupportWorkflow(db, actions):
        pass  # Actual schema setup, not a health-only pretend application.
    server = LocalWorkflowServer(("127.0.0.1", args.port), tokens=tokens, db=db, actions=actions,
                                 deadline=args.deadline, max_workers=args.max_workers)
    def stop(signum, frame):
        if not server.stopping.is_set():
            server.stopping.set()
            event("stopping", signal=signum)
            threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    event("listening", host="127.0.0.1", port=server.server_port,
          deadline_seconds=args.deadline, max_workers=args.max_workers)
    try:
        server.serve_forever(poll_interval=0.1)
    finally:
        server.stopping.set()
        server.server_close()
        event("stopped")


if __name__ == "__main__":
    main()
