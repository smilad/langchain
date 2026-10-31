# Teaching guide: detailed learning without tutorial dependence

Use with [the mission](../MISSION.md), [the roadmap](../ROADMAP.md), and [the source guide](../RESOURCES.md). This is an authoring/assessment specification, not evidence that a learner has completed a lesson.

## 1. What “highly detailed” means

A detailed lesson explains the mental model, the data/control flow, why an API is used, what it guarantees, where it fails, and how to inspect it. It does not introduce every adjacent API at once.

Separate three layers:

- **Lesson:** one observable skill, a small worked example, and its explanation.
- **Lab:** run the behavior, inspect intermediate state, vary a constraint, and diagnose a failure.
- **Reference:** concise terminology, verified API shapes, compatibility notes, and troubleshooting that can be reused later.

Authoring default: 15–25 minutes for the explanation/example and 30–60 minutes for a small lab segment, with larger project work split across sessions. These timings are adjustable design choices, not limits established by working-memory research.

## 2. Evidence-informed design

| Principle | Concrete implementation | Important limit |
|---|---|---|
| Retrieval practice | Begin with 2–3 short earlier-topic prompts; learner answers before seeing corrections. Ask for data flow, prediction, or explanation rather than memorized imports. | [Dunlosky et al.](https://acs.ist.psu.edu/ist521/dunloskyRMNW13.pdf) support retrieval/distributed practice broadly, not a guarantee of adult coding transfer. |
| Spaced practice | Reuse the concept next session, roughly a week later, and in a later project; vary the question and adjust after errors. | [Cepeda et al.](https://pubmed.ncbi.nlm.nih.gov/19076480/) show timing depends on retention horizon. This schedule is an initial policy, not a universal optimum. |
| Worked examples with fading | Show one small complete solution, remove its final meaningful step, then remove more support before a fresh task. Ask why each boundary exists. | [Renkl & Atkinson](https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/Structuring%20the%20Transition%20From%20Example%20Study%20to%20Problem%20Solving.pdf) do not establish automatic far transfer from completing blanks. |
| Explanatory questions | Connect a concrete observed value to its abstraction: message, tool call, retrieved document, state update, checkpoint. | [IES practice guide](https://files.eric.ed.gov/fulltext/ED498555.pdf) offers evidence-graded recommendations, not a rigid course recipe. |
| Informative feedback | Name the intended contract, the observed mismatch, and the next diagnostic action after a genuine attempt. | [Hattie & Timperley](https://assess.ucr.edu/sites/default/files/2019-02/hattietimperley_2007.pdf) distinguish useful task/process feedback from generic praise; timing effects vary. |
| Mastery-oriented progression | Fix objectives while allowing time/support to vary; correct a missed criterion and reassess with a fresh equivalent task. | [EEF mastery review](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/mastery-learning) concerns school contexts with limited evidence security, not an adult-course productivity forecast. |

Interleave already introduced skills during later practice—for example, compare a tool result, model message, and retrieved passage. Do not mix several unfamiliar topics into the first explanation. Assess actual delayed performance rather than claiming a teaching technique worked because it was used.

## 3. Required lesson structure

Each lesson file must contain the following, adapted to its single objective:

1. **Mission link and objective.** State a behavior: “Diagnose a retrieval miss by inspecting the retrieved passages,” not “Understand RAG.”
2. **Prerequisites.** Link to earlier concepts and give one small check; do not invent the learner's prior knowledge.
3. **Source and version note.** Primary URL, date checked, Python/dependency versions actually exercised, required model capabilities, and any credentials/cost.
4. **Retrieval warm-up.** Two or three earlier-topic questions, with corrections available only after an attempt.
5. **Mental model.** Explain responsibilities and boundaries before presenting syntax.
6. **Data/control-flow view.** Use a diagram or table where it makes an actual structure clearer. Include the shape of inputs, outputs, and intermediate values.
7. **Worked example.** Small runnable behavior, rationale alongside relevant steps, and observed output clearly distinguished from illustrative output.
8. **Guided completion.** Remove a meaningful step and ask the learner to supply it. Explain why it belongs there.
9. **Independent exercise.** Change input, schema, evidence, state, or another constraint. Link to the exercise file, not an inline answer.
10. **Failure investigation.** Include an in-scope fault; ask for a prediction and hypothesis before running it.
11. **Exit check.** Practical behavior, explanation, diagnosis, and independent variation. Keep model variability distinct from deterministic contract checks.
12. **Review and reference.** Name a later review opportunity, link relevant glossary/API entries, and invite a focused follow-up question.

The lab README additionally states setup commands, the actual entrypoint, input cases, expected behavior, observed evidence, provider limitations, and how to remove/reset local state safely. Mark commands as planned until they have been implemented and exercised.

## 4. Feedback and hints

### Hint ladder

Offer the least revealing support that permits another genuine attempt:

1. Ask the learner to identify the failed stage and its expected input/output.
2. Point to a trace, intermediate value, or documentation section.
3. Explain the specific concept or contract they missed.
4. Show a smaller analogous example.
5. Provide the worked solution only after an attempt or an explicit request.

Record support used. Completion with a supplied solution is practice, not evidence of independent implementation.

### Feedback format

**Goal → observation → cause/hypothesis → next action.**

Example: “The answer must be supported by retrieved passages. Your response cites source P3, but the trace contains P1 and P2 only. Inspect the source-ID propagation between retrieval and response construction; regenerate only after the citations can be checked against actual evidence.”

Avoid “Try again,” “Great job,” or “The model is wrong” as the complete explanation. Distinguish environmental failures, missing prerequisites, logic defects, and stochastic model errors; they need different interventions.

For novices, feedback soon after an authentic attempt is the default. Delay revealing answers long enough for the learner to reason; do not claim immediate feedback is optimal in every situation.

## 5. Mastery rubric

Use criterion-based decisions rather than averaging away a serious misconception.

| Dimension | Evidence required | Not sufficient |
|---|---|---|
| Practical execution | Actual lab meets the module's stated behavior, including named failure cases | Notebook cell runs once; test mocks echo the intended result |
| Conceptual explanation | Learner explains essential responsibilities/boundaries and limitations in their own words | Repeats the lesson definition or memorizes an import |
| Diagnosis | Learner predicts, inspects evidence, identifies a cause, and explains a repair | Changes prompts/parameters repeatedly until something works |
| Independent variation | Learner meets the objective under one changed constraint without copying the worked solution | Re-runs the exact example or has an assistant write the entire solution |
| Delayed retention | Later fresh recall plus a small documentation-allowed coding variation | Same-session fluency alone |

**Initial gate:** all first four criteria and the module-specific gate must be demonstrated. A missing security/state/evidence boundary cannot be offset by a high quiz score. Documentation lookup is allowed for realistic coding tasks; conceptual recall checks are short and closed-note.

**Retention:** initial mastery remains provisional until a later check. Continue unrelated work while waiting for the review, but remediate a delayed miss before major dependent project work. Do not silently label the prerequisite permanently learned.

**Reassessment:** identify the exact missed criterion, reteach only the relevant concept, then use a different equivalent task. More time/support is allowed; repeated access to the same answer is not reassessment.

**Assessment validity:** unavailable credentials, network/provider outages, or billing limits are environment blockers, not evidence of conceptual incompetence. Mark live execution unverified and record reachable conceptual/deterministic evidence separately; never replace the missing behavior with fake success.

## 6. Detailed lesson blueprint: supported citations in RAG

This blueprint demonstrates the authoring method; [Module 07](../lessons/07_rag/01.md) now implements the evidence-first RAG lesson and lab. Local boundaries are exercised; generated claim support still requires the live and human-review evidence described in [verification](VERIFICATION.md).

**Objective:** Given a question, retrieved passages, and an answer with source IDs, determine whether each substantive claim is supported and identify an appropriate abstention.

**Prerequisites:** document metadata, retrieval inspection, schema validation, and the difference between generated text and evidence.

**Primary sources:** the semantic-search tutorial and RAG evaluation tutorial in [RESOURCES.md](../RESOURCES.md).

**Mental model:** ingestion establishes source identity; retrieval selects passages; generation proposes an answer; verification checks whether the proposed claims are supported. A citation label alone does not verify a claim.

**Warm-up prompts:**
- If the retriever returns no relevant passage, can schema validation make the answer factual?
- What information must survive chunking for a learner to locate the original source?

**Worked case design:** use synthetic policy P1 stating a return period, P2 stating a different condition, and P3 with an outdated date. Inspect actual retrieved text before presenting the generated answer. Explain which claim uses which passage and why the version matters.

**Fading task:** provide the proposed answer and retrieved passages but omit the claim-to-source mapping. The learner supplies the mapping and identifies unsupported claims.

**Independent variation:** change the question so the corpus does not contain the answer. The learner designs an abstention without inventing a policy or citing an irrelevant passage.

**Failure investigation:** intentionally lose source metadata during ingestion, or pair a valid source ID with a passage that does not support the claim. Require inspection of the ingestion/retrieval/output boundary rather than prompt tweaking alone.

**Gate:** actual sources are present in retrieval, cited claims are supported, unavailable evidence produces abstention, and the learner can distinguish source-ID validity from factual support. Repeat with a different question during Module 08 evaluation.

**Limit:** automated checks can verify IDs/schema membership; semantic support requires an explicit rubric, human review, or a calibrated evaluator. A model judge is not an infallible source of truth.

## 7. Learning records and progress

Use the `teach` skill's useful distinction: coverage is not learning. Create `learning-records/` lazily, only after a real learner demonstration. Do not create fictional progress records during course authoring.

A record should capture:
- The non-obvious concept, corrected misconception, or established prior knowledge.
- Evidence: task/input, observed behavior, explanation, and hints used.
- Implications: what this unlocks and what still needs review.
- A later review opportunity if retention has not yet been demonstrated.

Use sequential files such as `0001-retrieval-is-not-groundedness.md`. If a later insight corrects an earlier record, mark the earlier one superseded rather than losing the history. Keep ordinary session logs separate; do not inflate them into mastery evidence.

The mission changes only when the user changes the goal; a teacher's preference for a new framework is not a mission change.

## 8. AI-assisted teaching rules

An assistant is a coach and source-checking partner, not a substitute for learner evidence.

- Before explanation, inspect demonstrated prerequisites and ask one focused question when a misconception is unresolved.
- Cite actual sources; say when an API/version/capability has not been checked.
- During practice, ask for a prediction or attempt before supplying the solution.
- Use the hint ladder and respond to the learner's actual reasoning, not a canned answer.
- Ask “why this component?” and “what would break under this changed constraint?” after a passing run.
- Never mark an AI-generated implementation as the learner's independent work.
- Record observed understanding and uncertainty honestly. A learner saying “got it” is useful feedback, not a durable-mastery gate.

Suggested practice request: “Coach me through the Module 06 retrieval exercise. Ask for my prediction first, provide one hint at a time, inspect my retrieved passages, and do not reveal the solution until I attempt it. Use the module sources and report unverified assumptions.”

## 9. Quality checklist before publishing a module

- [ ] Mission, single-lesson objectives, and prerequisites are explicit.
- [ ] Four lessons cover the module topics without skipping its practical gate.
- [ ] Official source URLs, exercised versions, provider capabilities, and costs/credentials are stated.
- [ ] The real lab ran; named normal/failure cases were observed and limitations recorded.
- [ ] Exercises require a changed constraint; solutions are separate and explained.
- [ ] Feedback identifies reasoning/contracts rather than only a pass/fail result.
- [ ] Stochastic model behavior is evaluated separately from deterministic logic.
- [ ] Private data and secrets are absent from committed examples and trace evidence.
- [ ] Local links and commands point to implemented files, not future placeholders.
- [ ] Glossary/reference entries reflect the APIs actually taught; obsolete paths are not promoted as the new default.
- [ ] Later retrieval/transfer checks are scheduled without claiming a universal review interval.
- [ ] Learning progress is recorded only when demonstrated by the learner.
