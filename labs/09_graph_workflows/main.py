"""Actual graph routes, parallel reducers, and optional provider classification."""
from operator import add
from typing import Annotated, Literal, TypedDict

from langgraph.errors import GraphRecursionError, InvalidUpdateError
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import emit, get_model, lab_parser, preflight, run_lab


class Route(BaseModel):
    route: Literal["supported", "review", "unsupported"]


class RequestState(TypedDict, total=False):
    question: str
    user_id: str
    route: str
    evidence: list[dict]
    events: Annotated[list[str], add]
    draft: str
    draft_origin: str
    status: str


def build_graph(*, live=False, broken_reducer=False):
    def classify(state):
        if live:
            result = get_model().with_structured_output(Route).invoke([
                {"role": "system", "content": "Classify a support request: policy questions supported; requests to act or escalate review; unrelated topics unsupported. Classify only, do not act."},
                {"role": "user", "content": state["question"]},
            ])
            route = result.route
        else:
            # Explicit routing fixtures teach control flow, not model quality.
            route = "review" if "escalate" in state["question"].lower() else "supported" if "return" in state["question"].lower() else "unsupported"
        return {"route": route, "events": ["classify:" + route]}

    def retrieve(state):
        documents = PolicyIndex().search(state["question"], state["user_id"])
        return {"evidence": [{"text": doc.page_content, "metadata": doc.metadata} for doc in documents], "events": ["retrieve"]}

    def constraints(state):
        return {"events": ["constraint:read_only"]}

    def draft(state):
        if live:
            from langchain_learning.rag import answer
            result = answer(state["question"], state["user_id"])
            return {"draft": result.answer, "draft_origin": "model", "status": "drafted", "events": ["draft"]}
        return {"draft": "Human routing exercise: review the retrieved policy before replying.", "draft_origin": "human", "status": "drafted", "events": ["draft"]}

    def review(state):
        return {"status": "human_review_required", "events": ["review"]}

    def unsupported(state):
        return {"status": "unsupported", "events": ["unsupported"]}

    if broken_reducer:
        class BrokenState(TypedDict, total=False):
            question: str
            user_id: str
            route: str
            evidence: list[dict]
            events: list[str]
            draft: str
            draft_origin: str
            status: str
        builder = StateGraph(BrokenState)
    else:
        builder = StateGraph(RequestState)
    for name, node in (("classify", classify), ("retrieve", retrieve), ("constraints", constraints), ("draft", draft), ("review", review), ("unsupported", unsupported)):
        builder.add_node(name, node)
    builder.add_edge(START, "classify")
    builder.add_conditional_edges("classify", lambda state: ["retrieve", "constraints"] if state["route"] == "supported" else state["route"], {"retrieve": "retrieve", "constraints": "constraints", "review": "review", "unsupported": "unsupported"})
    builder.add_edge(["retrieve", "constraints"], "draft")
    for name in ("draft", "review", "unsupported"):
        builder.add_edge(name, END)
    return builder.compile()


def check():
    graph = build_graph()
    results = []
    for question, expected in (("What is the return policy?", "drafted"), ("Please escalate this request", "human_review_required"), ("Describe Saturn", "unsupported")):
        initial = {"question": question, "user_id": "alice", "events": []}
        updates = list(graph.stream(initial, {"recursion_limit": 8}, stream_mode="updates"))
        result = graph.invoke(initial, {"recursion_limit": 8})
        assert result["status"] == expected
        if expected == "drafted":
            assert {"retrieve", "constraint:read_only"} <= set(result["events"])
        results.append({"question": question, "updates": updates, "state": result})
    try:
        build_graph(broken_reducer=True).invoke({"question": "return policy", "user_id": "alice", "events": []})
    except InvalidUpdateError:
        reducer_failure = "Actual parallel writes without reducer rejected"
    else:
        raise AssertionError("Missing reducer was not rejected")
    loop = StateGraph(dict)
    loop.add_node("again", lambda state: {})
    loop.add_edge(START, "again")
    loop.add_edge("again", "again")
    try:
        loop.compile().invoke({}, {"recursion_limit": 3})
    except GraphRecursionError:
        termination_failure = "Actual nonterminating graph reached recursion limit"
    else:
        raise AssertionError("Nonterminating graph did not stop")
    return {"routes": results, "reducer_failure": reducer_failure, "termination_failure": termination_failure, "live_gate": "Unverified: real model classification and grounded drafting require --live"}


def main():
    parser = lab_parser(__doc__)
    parser.add_argument("--question", default="What is the return policy?")
    args = parser.parse_args()
    emit({"preflight": preflight()})
    if args.live:
        emit(build_graph(live=True).invoke({"question": args.question, "user_id": "alice", "events": []}, {"recursion_limit": 8}))
    else:
        emit(check())


if __name__ == "__main__":
    run_lab(main)
