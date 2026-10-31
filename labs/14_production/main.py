"""Operate an actual localhost service through HTTP, including restart and disconnect."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import uuid

from langchain_learning.runtime import ROOT, emit, lab_parser, load_environment, model_settings, preflight, run_lab


def call(base: str, token: str | None, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(base + path, data=None if body is None else json.dumps(body).encode(),
                      headers=headers, method=method)
    try:
        with urlopen(request, timeout=40) as response:
            return response.status, json.load(response)
    except HTTPError as exc:
        return exc.code, json.load(exc)


@contextmanager
def service(root: Path, tokens: dict, *, environment: dict | None = None, deadline: float = 30):
    with socket.socket() as reserve:
        reserve.bind(("127.0.0.1", 0))
        port = reserve.getsockname()[1]
    env = {**os.environ, "COURSE_STATE_DIR": str(root), "COURSE_AUTH_TOKENS": json.dumps(tokens),
           **(environment or {})}
    with tempfile.TemporaryFile(mode="w+") as logs:
        process = subprocess.Popen([sys.executable, "-m", "langchain_learning.service", "--port", str(port),
                                    "--deadline", str(deadline)], cwd=ROOT, env=env,
                                   stdout=subprocess.DEVNULL, stderr=logs)
        base = f"http://127.0.0.1:{port}"
        try:
            for attempt in range(100):
                if process.poll() is not None:
                    raise RuntimeError("Local service failed during startup; run service entrypoint for sanitized diagnostics")
                try:
                    status, ready = call(base, None, "GET", "/ready")
                    if status == 200 and ready["ready"]:
                        break
                except (URLError, TimeoutError, ConnectionError):
                    pass  # Startup readiness polling only, not swallowed workflow errors.
                time.sleep(0.1)
            else:
                raise TimeoutError("Local service did not become ready")
            yield base, port
        finally:
            if process.poll() is None:
                process.send_signal(signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                raise RuntimeError("Service required forced shutdown") from None
            logs.seek(0)
            # Server structured event logs intentionally contain no bearer/content/provider text.
            events = []
            for line in logs:
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict) and "event" in value:
                    events.append(value)
            emit({"service_events": events, "exit_code": process.returncode})
            if process.returncode != 0:
                raise RuntimeError("Service exited unsuccessfully")


def expect(status: int, expected: int, value: dict) -> dict:
    if status != expected:
        raise AssertionError(f"Expected HTTP {expected}, received {status}; error={value.get('error', 'none')}")
    return value


def cancellation(base: str, port: int, token: str) -> dict:
    request_id = "cancel-" + uuid.uuid4().hex
    payload = json.dumps({"thread_id": request_id, "question": "Human cancellation experiment",
                          "draft": "Human-authored draft; do not send."}).encode()
    with socket.create_connection(("127.0.0.1", port), timeout=5) as connection:
        connection.sendall((f"POST /threads/start HTTP/1.0\r\nAuthorization: Bearer {token}\r\n"
                            f"X-Request-ID: {request_id}\r\nContent-Type: application/json\r\n"
                            f"Content-Length: {len(payload)}\r\n\r\n").encode() + payload)
        connection.shutdown(socket.SHUT_RDWR)
    for attempt in range(60):
        status, value = call(base, token, "GET", "/requests/" + request_id)
        if status == 200 and value["result"]["status"] != "running":
            break
        time.sleep(0.1)
    else:
        raise AssertionError("Disconnect did not become visible")
    if value["result"]["status"] not in {"cancelled", "response_disconnected"}:
        raise AssertionError("Expected actual disconnect outcome, not synthetic success")
    thread_status, thread = call(base, token, "GET", "/threads/" + request_id)
    return {"request_outcome": value, "persisted_thread_http_status": thread_status,
            "persisted_thread": thread, "interpretation": "Cancelled response is not a rollback guarantee."}


def main() -> None:
    args = lab_parser(__doc__).parse_args()
    load_environment()
    emit({"preflight": preflight()})
    if args.live:
        model_settings()
    alice, bob = secrets.token_urlsafe(24), secrets.token_urlsafe(24)
    tokens = {alice: "alice", bob: "bob"}
    with tempfile.TemporaryDirectory(prefix="course-http-") as directory:
        root = Path(directory)
        with service(root, tokens) as (base, port):
            status, value = call(base, None, "GET", "/health")
            expect(status, 200, value)
            status, value = call(base, None, "GET", "/threads/a")
            expect(status, 401, value)
            cases = [(alice, "alice-thread", "Draft explicitly written by Alice"),
                     (bob, "bob-thread", "Draft explicitly written by Bob")]
            def start(case):
                token, thread, draft = case
                status, value = call(base, token, "POST", "/threads/start",
                                     {"thread_id": thread, "question": "What is the return policy?", "draft": draft})
                return expect(status, 200, value)
            with ThreadPoolExecutor(max_workers=2) as executor:
                started = list(executor.map(start, cases))
            if any(row["result"]["status"] != "pending" for row in started):
                raise AssertionError("Human workflows did not pause for review")
            status, value = call(base, bob, "GET", "/threads/alice-thread")
            expect(status, 403, value)
            status, value = call(base, alice, "POST", "/threads/start",
                                 {"thread_id": "identity-attack", "question": "test", "draft": "test", "user_id": "bob"})
            expect(status, 400, value)
            emit({"concurrent_starts": started, "body_identity_rejected": True,
                  "cross_identity_denied": True, "cancellation": cancellation(base, port, alice)})
            if args.live:
                status, value = call(base, alice, "POST", "/threads/start",
                                     {"thread_id": "live-rag", "question": "What is the returns deadline for an unused item?", "live": True})
                emit({"live_rag": expect(status, 200, value)})
        # Real subprocess shutdown/restart against the same SQLite files.
        with service(root, tokens) as (base, port):
            status, value = call(base, alice, "GET", "/threads/alice-thread")
            pending = expect(status, 200, value)
            if pending["result"]["status"] != "pending":
                raise AssertionError("Pending state lost across process restart")
            for attempt in range(2):
                status, value = call(base, alice, "POST", "/threads/alice-thread/decision", {"decision": "approve"})
                expect(status, 200, value)
            status, value = call(base, bob, "POST", "/threads/bob-thread/decision", {"decision": "reject"})
            expect(status, 200, value)
            status, value = call(base, alice, "GET", "/actions")
            actions = expect(status, 200, value)
            if len(actions["result"]) != 1:
                raise AssertionError("Replay duplicated approved action")
            status, value = call(base, bob, "GET", "/actions")
            if expect(status, 200, value)["result"]:
                raise AssertionError("Rejected workflow recorded an action")
            emit({"restart_pending": pending, "idempotent_actions": actions, "rejection_actions": []})
        if args.live:
            # Actual unreachable provider endpoint with genuine configured credentials.
            # No synthetic API key and no fabricated provider response.
            with service(root, tokens, environment={"OPENAI_BASE_URL": "http://127.0.0.1:1/v1"}) as (base, port):
                status, value = call(base, alice, "POST", "/threads/start",
                                     {"thread_id": "upstream-failure", "question": "What is the returns deadline for an unused item?", "live": True})
                expect(status, 502, value)
                emit({"upstream_transport_failure": value})
        else:
            with service(root, tokens, environment={"COURSE_ALLOW_LIVE": "0"}) as (base, port):
                status, value = call(base, alice, "POST", "/threads/start",
                                     {"thread_id": "live-not-authorized", "question": "What is the return policy?", "live": True})
                if status not in {400, 403}:
                    raise AssertionError("Unconsented model invocation did not visibly fail")
                emit({"missing_live_permission": value,
                      "live_gate": "Unverified: real RAG and provider outage require genuine model configuration."})
        with service(root, tokens, deadline=0.1) as (base, port):
            status, value = call(base, alice, "POST", "/threads/start",
                                 {"thread_id": "deadline", "question": "Human deadline trial", "draft": "Human draft"})
            if status not in {200, 504}:
                raise AssertionError("Unexpected deadline trial response")
            emit({"deadline_trial_http_status": status, "response": value,
                  "note": "A very fast machine may finish inside the deadline; lower bounds prevent zero deadlines."})
    emit({"local_state": "Temporary lab state removed after service shutdown; persistent manual service state is untouched."})


if __name__ == "__main__":
    run_lab(main)
