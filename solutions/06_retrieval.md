# Module 06 solutions — retrieved text must be inspectable

Attempt [the exercises](../exercises/06_retrieval.md) first. These are reasoning guides, not fabricated transcript screenshots. See [verification](../docs/VERIFICATION.md) for exercised paths.

## 1. Provenance

`PolicyIndex.refresh()` reads policy JSON into actual LangChain `Document` instances. The source ID groups versions; `version` distinguishes policy revisions; `current` selects active records; `audience` controls eligible identities; `trust` distinguishes policy authority from an untrusted fixture. The path maps back to the file. `content_sha256` changes when source text changes. `chunk_id` is source ID + version + ordinal; neither a low ordinal nor a hash implies reliability. A chunk's page content is the evidence to read, not merely its ID.

## 2. Ranking and misses

The local index uses actual TF-IDF cosine relevance, not pretend embeddings. `returns` and an exact `SHIP-42` identifier can share useful tokens with sources. A reimbursement paraphrase can miss because synonyms do not share tokens; a lunar-habitat question can yield no evidence. Read the actual ranked passages before declaring either method successful. A learned embedding requires a real embedding request; retrieving k passages is not proof any passage answers the question.

## 3. Splitting

The transparent splitter uses character windows, overlap, and a nearby sentence break. Compare the whole condition-bearing passage with fragments at the smaller limit. Too-small chunks can lose the relationship between eligibility and deadline; overlap can preserve it but increases duplication. Choose a chunk size from actual question/evidence behavior, not a universal magic number. Preserve metadata on every resulting chunk.

## 4. Freshness

The lab edits a temporary copy from thirty to thirty-seven days and verifies no retrieved current return chunk retains the old text. Refresh hashes file payloads, replaces the document set, and clears vector-store caches on change; it does not append another stale set. Removing a current file leaves the obsolete file excluded because its flag remains false. Duplicate source versions or two current records for the same source are explicit ingestion errors. Do not modify the frozen benchmark to improve a score.

## 5. Access

`authorized_documents()` restricts to current records and the caller's authorized audiences before ranking or creating the embedding store. Alice/Bob cannot retrieve finance-only sources; finance can. Unknown IDs fail closed. A public irrelevant hit is not a confidentiality leak, but is still poor relevance. Embedding confidential text first and filtering the final list later would disclose content to an external service before the permission decision.

## 6. Semantic comparison

Use explicit consent, key, and embedding-model ID. Compare exact identifiers and paraphrases with the same corpus and k. Report relevance, misses, timing and provider usage availability; hybrid reciprocal-rank fusion changes ranking, not authorization. Without credentials, the valid conclusion is local retrieval/provenance/access verified and learned semantic behavior unverified.
