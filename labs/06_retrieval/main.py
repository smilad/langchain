"""Inspect real ingestion/retrieval; remote embedding only with explicit --live."""
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import DATA, emit, lab_parser, preflight, run_lab


def main():
    parser = lab_parser(__doc__)
    parser.add_argument("--query", default="What is the returns deadline?")
    parser.add_argument("--user", default="alice")
    parser.add_argument("--strategy", choices=["lexical", "semantic", "hybrid"], default="lexical")
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()
    emit({"preflight": preflight()})
    if not args.live and args.strategy != "lexical":
        raise ValueError("Use --live for actual OpenAI semantic/hybrid search")
    index = PolicyIndex(args.strategy)
    queries = [args.query, "SHIP-42", "money back for dinner while travelling", "quasar lunar habitat"]
    results = [{"query": q, "documents": index.as_retriever(args.user, k=args.k).invoke(q)} for q in queries]
    # Run a real source edit in a disposable copy, never alter the committed benchmark.
    with TemporaryDirectory(prefix="course-policies-") as temporary:
        directory = Path(temporary)
        for source in (DATA / "policies").glob("*.json"):
            shutil.copyfile(source, directory / source.name)
        edited = PolicyIndex(directory=directory)
        before = edited.search("returns", "alice")
        source = directory / "return-v2.json"
        record = json.loads(source.read_text())
        record["text"] = "Returns are accepted within 37 calendar days of delivery with a receipt. Items must be unused."
        source.write_text(json.dumps(record))
        after = edited.search("returns", "alice")
        return_docs = [d for d in after if d.metadata["source_id"] == "RETURN"]
        if not return_docs or any("30 calendar" in d.page_content for d in return_docs):
            raise ValueError("Source edit left obsolete text")
        edit_evidence = {"before": before, "after": after, "fingerprint": edited.fingerprint}
    public = index.search("finance reserve code", "alice", k=10)
    if any(d.metadata["audience"] != "public" or not d.metadata["current"] for d in public):
        raise ValueError("Unauthorized/outdated source retrieved")
    rejected = False
    try:
        index.search("returns", "unknown")
    except PermissionError:
        rejected = True
    if not rejected:
        raise ValueError("Unknown identity was granted access")
    emit({"searches": results, "source_edit": edit_evidence, "unknown_identity_rejected": rejected,
          "public_finance_query": public, "live_embedding_exercised": args.live and args.strategy != "lexical",
          "limits": "Lexical does not understand synonyms; semantic top-k may return irrelevant documents. No generated answers here."})


if __name__ == "__main__":
    run_lab(main)
