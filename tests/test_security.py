"""Exercise owned and forbidden reads through the real tool runtime, without a model."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from langchain_learning.security import SecurityContext, inspect_thread
from langchain_learning.workflow import SupportWorkflow


class SecurityToolTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        self.db, self.actions = root / "state.sqlite", root / "actions.sqlite"
        with SupportWorkflow(self.db, self.actions) as flow:
            flow.start("alice", "alice-thread", "Private question", draft="Private human draft")
        builder = StateGraph(MessagesState, context_schema=SecurityContext)
        builder.add_node("tools", ToolNode([inspect_thread], handle_tool_errors=False))
        builder.add_edge(START, "tools")
        builder.add_edge("tools", END)
        self.graph = builder.compile()

    def inspect(self, user):
        # An authored tool request drives actual dispatch; no provider response is mocked.
        return self.graph.invoke(
            {"messages": [AIMessage(content="", tool_calls=[{
                "name": "inspect_thread", "args": {"thread_id": "alice-thread"},
                "id": "authored-read", "type": "tool_call",
            }])]},
            context=SecurityContext(user, self.db, self.actions),
        )

    def test_owned_thread_returns_minimal_pending_status(self):
        result = json.loads(self.inspect("alice")["messages"][-1].content)
        self.assertEqual(result, {"thread_id": "alice-thread", "status": "pending",
                                  "pending_review_count": 1, "action_count": 0})

    def test_foreign_thread_is_denied_without_changing_review(self):
        with self.assertRaises(PermissionError):
            self.inspect("bob")
        with SupportWorkflow(self.db, self.actions) as flow:
            self.assertEqual(flow.inspect("alice", "alice-thread")["status"], "pending")
            self.assertEqual(flow.actions("alice"), [])
