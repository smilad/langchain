"""Durable local approval; exactly-once applies only to the atomic SQLite sink."""
from __future__ import annotations

import fcntl
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import TypedDict
from uuid import uuid4

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class SupportState(TypedDict, total=False):
    user_id: str
    thread_id: str
    question: str
    draft: str
    draft_origin: str
    source_ids: list[str]
    live: bool
    action_id: str
    decision: str
    status: str


class SupportWorkflow:
    """One context per request. Local POSIX file locking serializes graph runs.

    Identity is a trusted caller argument, not authentication in itself. HTTP
    callers must authenticate before supplying it. Both databases are private
    application files, not an interface for untrusted clients.
    """

    def __init__(self, db_path: Path, actions_path: Path):
        self.db_path = Path(db_path).resolve()
        self.actions_path = Path(actions_path).resolve()
        if self.db_path == self.actions_path:
            raise ValueError("Checkpoint and action databases must be distinct")
        self._conn = None
        self._sink = None
        self._lock_file = None
        self._graph = None

    def __enter__(self):
        if self._conn is not None:
            raise ValueError("Workflow is already open")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.actions_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_file = open(str(self.db_path) + ".lock", "a+b")
        try:
            with self._locked():
                self._conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
                self._sink = sqlite3.connect(self.actions_path, timeout=30, check_same_thread=False)
                self._sink.row_factory = sqlite3.Row
                self._conn.execute("CREATE TABLE IF NOT EXISTS course_binding (id INTEGER PRIMARY KEY CHECK(id=1), actions_path TEXT NOT NULL)")
                with self._conn:
                    self._conn.execute("INSERT OR IGNORE INTO course_binding VALUES (1, ?)", (str(self.actions_path),))
                bound = self._conn.execute("SELECT actions_path FROM course_binding WHERE id=1").fetchone()[0]
                if bound != str(self.actions_path):
                    raise ValueError("Checkpoint database is bound to a different action database")
                self._sink.executescript("""
                    PRAGMA journal_mode=WAL;
                    CREATE TABLE IF NOT EXISTS support_threads (
                        thread_id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
                        action_id TEXT UNIQUE NOT NULL, initial_input TEXT NOT NULL,
                        decision TEXT, edited_draft TEXT
                    );
                    CREATE TABLE IF NOT EXISTS support_actions (
                        action_id TEXT PRIMARY KEY, thread_id TEXT UNIQUE NOT NULL,
                        user_id TEXT NOT NULL, draft TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                self._graph = self._build(SqliteSaver(self._conn))
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, exc_type, exc, tb):
        for connection in (self._sink, self._conn):
            if connection is not None:
                connection.close()
        if self._lock_file is not None:
            self._lock_file.close()
        self._sink = self._conn = self._lock_file = self._graph = None

    @contextmanager
    def _locked(self):
        if self._lock_file is None:
            raise ValueError("Use SupportWorkflow as a context manager")
        fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _text(value: str, label: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} must be nonempty text")
        if len(value) > 20_000:
            raise ValueError(f"{label} is too long")
        return value

    def _owner(self, user_id: str, thread_id: str):
        self._text(user_id, "User ID")
        self._text(thread_id, "Thread ID")
        row = self._sink.execute("SELECT * FROM support_threads WHERE thread_id=?", (thread_id,)).fetchone()
        if row is None:
            raise ValueError("Thread does not exist")
        if row["user_id"] != user_id:
            raise PermissionError("Thread access denied")
        return row

    @staticmethod
    def _config(thread_id):
        return {"configurable": {"thread_id": thread_id}, "recursion_limit": 12}

    def _build(self, saver):
        def draft_node(state):
            if state["draft_origin"] == "human":
                return {"status": "pending"}
            from langchain_learning.rag import answer
            grounded = answer(state["question"], state["user_id"])
            return {"draft": grounded.answer, "source_ids": grounded.source_ids, "status": "pending"}

        def review_node(state):
            response = interrupt({"kind": "support_review", "draft": state["draft"], "draft_origin": state["draft_origin"], "source_ids": state.get("source_ids", []), "allowed_decisions": ["approve", "reject", "edit"]})
            row = self._owner(state["user_id"], state["thread_id"])
            if response != {"decision": row["decision"], "edited_draft": row["edited_draft"]}:
                raise PermissionError("Resume does not match persisted human decision")
            decision = row["decision"]
            if decision not in {"approve", "reject", "edit"}:
                raise ValueError("Human decision is missing")
            draft = row["edited_draft"] if decision == "edit" else state["draft"]
            return {"decision": decision, "draft": draft, "status": "rejected" if decision == "reject" else "approved"}

        def record_node(state):
            self._record_action(state)
            return {"status": "recorded"}

        builder = StateGraph(SupportState)
        builder.add_node("draft", draft_node)
        builder.add_node("review", review_node)
        builder.add_node("record", record_node)
        builder.add_edge(START, "draft")
        builder.add_edge("draft", "review")
        builder.add_conditional_edges("review", lambda state: "reject" if state["decision"] == "reject" else "record", {"reject": END, "record": "record"})
        builder.add_edge("record", END)
        return builder.compile(checkpointer=saver)

    def _record_action(self, state):
        row = self._owner(state["user_id"], state["thread_id"])
        if row["decision"] not in {"approve", "edit"} or state["decision"] != row["decision"] or state["action_id"] != row["action_id"]:
            raise PermissionError("Action is not authorized")
        if row["decision"] == "edit" and state["draft"] != row["edited_draft"]:
            raise PermissionError("Action differs from approved edit")
        with self._sink:
            self._sink.execute("INSERT OR IGNORE INTO support_actions (action_id, thread_id, user_id, draft) VALUES (?, ?, ?, ?)", (state["action_id"], state["thread_id"], state["user_id"], state["draft"]))
            saved = self._sink.execute("SELECT * FROM support_actions WHERE action_id=?", (state["action_id"],)).fetchone()
            if saved is None or any(saved[key] != state[key] for key in ("thread_id", "user_id", "draft")):
                raise PermissionError("Action identity conflicts with an existing record")

    def start(self, user_id: str, thread_id: str, question: str, *, draft: str | None = None, live: bool = False) -> dict:
        for value, label in ((user_id, "User ID"), (thread_id, "Thread ID"), (question, "Question")):
            self._text(value, label)
        if draft is not None:
            self._text(draft, "Human draft")
        with self._locked():
            existing = self._sink.execute("SELECT user_id FROM support_threads WHERE thread_id=?", (thread_id,)).fetchone()
            if existing is not None:
                self._owner(user_id, thread_id)
                return self._inspect(user_id, thread_id)
            if draft is None and not live:
                raise ValueError("Supply an explicit human draft or enable live model drafting")
            if draft is None:
                from langchain_learning.runtime import model_settings
                model_settings()  # Validate live intent before creating any persisted request.
            initial = {"user_id": user_id, "thread_id": thread_id, "question": question, "draft": draft or "", "draft_origin": "human" if draft is not None else "model", "source_ids": [], "live": live, "action_id": uuid4().hex, "status": "running"}
            with self._sink:
                self._sink.execute("INSERT INTO support_threads (thread_id,user_id,action_id,initial_input) VALUES (?,?,?,?)", (thread_id, user_id, initial["action_id"], json.dumps(initial)))
            self._graph.invoke(initial, self._config(thread_id))
            return self._inspect(user_id, thread_id)

    def _inspect(self, user_id, thread_id):
        self._owner(user_id, thread_id)
        snapshot = self._graph.get_state(self._config(thread_id))
        pending = [item.value for task in snapshot.tasks for item in task.interrupts]
        state = dict(snapshot.values)
        records = self._sink.execute("SELECT * FROM support_actions WHERE thread_id=? AND user_id=?", (thread_id, user_id)).fetchall()
        return {"thread_id": thread_id, "user_id": user_id, "status": "pending" if pending else state.get("status", "running"), "state": state, "pending_review": pending, "actions": [dict(row) for row in records]}

    def inspect(self, user_id: str, thread_id: str) -> dict:
        with self._locked():
            return self._inspect(user_id, thread_id)

    def decide(self, user_id: str, thread_id: str, decision: str, *, edited_draft: str | None = None) -> dict:
        if decision not in {"approve", "reject", "edit"}:
            raise ValueError("Decision must be approve, reject, or edit")
        if decision == "edit":
            self._text(edited_draft, "Edited draft")
        elif edited_draft is not None:
            raise ValueError("Only edit accepts an edited draft")
        with self._locked():
            row = self._owner(user_id, thread_id)
            if row["decision"] is not None and (row["decision"], row["edited_draft"]) != (decision, edited_draft):
                raise ValueError("A human decision is already bound to this thread")
            config = self._config(thread_id)
            snapshot = self._graph.get_state(config)
            if not snapshot.values:
                self._graph.invoke(json.loads(row["initial_input"]), config)
                snapshot = self._graph.get_state(config)
            if not snapshot.next:
                return self._inspect(user_id, thread_id)
            if not any(task.interrupts for task in snapshot.tasks):
                # Recover an interrupted process/provider failure to the review boundary.
                self._graph.invoke(None, config)
                snapshot = self._graph.get_state(config)
                if not any(task.interrupts for task in snapshot.tasks):
                    return self._inspect(user_id, thread_id)
            with self._sink:
                self._sink.execute("UPDATE support_threads SET decision=?, edited_draft=? WHERE thread_id=? AND decision IS NULL", (decision, edited_draft, thread_id))
            self._graph.invoke(Command(resume={"decision": decision, "edited_draft": edited_draft}), config)
            return self._inspect(user_id, thread_id)

    def actions(self, user_id: str) -> list[dict]:
        self._text(user_id, "User ID")
        with self._locked():
            return [dict(row) for row in self._sink.execute("SELECT * FROM support_actions WHERE user_id=? ORDER BY created_at, action_id", (user_id,)).fetchall()]
