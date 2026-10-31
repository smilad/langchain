# Module 06 exercises — retrieval before generation

Start with [the lessons](../lessons/06_retrieval/01.md), [lab commands](../labs/06_retrieval/README.md), and [the glossary](../reference/GLOSSARY.md). Attempt these before [solutions](../solutions/06_retrieval.md). The installed versions and actual smoke limits are recorded in [verification](../docs/VERIFICATION.md).

## 1. Trace ingestion and provenance

Run `uv run python labs/06_retrieval/main.py --check`. Select a retrieved `Document` and explain `source_id`, `version`, `current`, `audience`, `trust`, `chunk_id`, and `content_sha256`. Map its text back to a file. Explain which metadata identifies an original source, a source version, and one chunk. Do not confuse the chunk ordinal with an authority ranking.

## 2. Predict four retrieval outcomes

Before executing, predict the evidence for `returns deadline`, `SHIP-42`, `money back for dinner while travelling`, and `quasar lunar habitat`. Then compare the actual passages with your prediction. Which miss follows from lexical token overlap? Which no-match must not be repaired by fabricating a document? Explain why a semantic top-k result may still be irrelevant.

## 3. Vary chunk boundaries

Use a disposable copy of the corpus and construct `PolicyIndex(directory=copy, chunk_size=200, overlap=40)`. Inspect the chunks and retrieved evidence for a question requiring an eligibility condition. Compare against the default split. Keep source provenance through both versions; explain why finding a deadline without its conditions can lead to a misleading answer.

## 4. Update and remove a source

In the disposable copy, change the current return text, search again, and demonstrate that the old text is gone. Remove that current source file and search again. The obsolete version must not become current merely because the current one disappeared. Finally create two current versions with the same source ID: ingestion must reject the ambiguous active source rather than silently pick one.

## 5. Test permissions before relevance

Query the finance reserve as Alice, Bob, and finance. Show which source IDs each identity can retrieve; unknown identities must raise `PermissionError`. Explain why filtering after a provider has embedded confidential text is too late. CLI user selection is a synthetic exercise, not production authentication.

## 6. Optional real semantic comparison

With explicit provider consent and an actual configured embedding model, run `--live --strategy semantic`. Compare a paraphrase and an exact identifier against lexical retrieval. Change only retrieval strategy and record evidence, latency, and usage limits. Without credentials, complete the local work and mark learned semantic-search behavior unverified—not mocked or replaced.

**Gate:** identify provenance, diagnose a lexical miss, demonstrate edit/removal without stale sources, enforce access boundaries, and explain the semantic comparison's remaining prerequisites. Revisit with a fresh question during RAG evaluation; record hints used rather than marking reading as mastery.
