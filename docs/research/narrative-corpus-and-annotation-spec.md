# Narrative Corpus and Annotation Specification

## Purpose and status

This document defines the research corpus and annotation protocol for the first Narrative Intelligence experiments. It builds on the repository's narrative model, intelligence architecture, product feature/screen maps, and architecture decisions. It does not replace those documents or introduce application schemas.

This is a research specification only. It does not modify application code, build UI, add APIs or database tables, train or fine-tune models, or acquire/ingest source material. No specific screenplay title is declared rights-cleared by this document.

Source documents:

- [Narrative model](../architecture/narrative-model.md)
- [Narrative intelligence architecture](../architecture/narrative-intelligence-architecture.md)
- [Narrative Lab feature map](../product/narrative-lab-feature-map.md)
- [Narrative Lab screen map](../product/narrative-lab-screen-map.md)
- [Narrative Lab architecture decisions](../product/narrative-lab-architecture-decisions.md)

The guiding goal is to represent what actual narrative works do, including variation, ambiguity, contradiction, unconventional structures, and alternative interpretations. The goal is not to create a textbook of screenplay rules.

## 1. Corpus principle

The corpus has two distinct layers:

| Corpus layer | Contains | Does not mean |
| --- | --- | --- |
| SOURCE CORPUS | Work and Source identities, governed original screenplay text or film references, provenance, source revisions, and rights/access metadata. | A fully analyzed or labeled set of Works. |
| STRUCTURED / ANNOTATED CORPUS | Source-aligned parser representation, canonical narrative objects and relations, Evidence, AnalysisClaims, dataset annotations, review outcomes, and approved comparative relations. | A replacement for the original source or a single unquestionable reading of it. |

Keep them separate so source material remains intact while analysis can be corrected, expanded, disputed, regenerated, or governed independently. Every annotation and claim must identify the source revision it concerns. The original source revision must never be overwritten after claims or annotations point to it. A changed source gets a new revision identity and retains the older source/payload identity for existing anchors.

“Dataset annotation” in this document means a research label produced under an annotation protocol. It is distinct from the product's user-generated Annotation object, which is private user material anchored to a Scene and/or source span. Dataset labels do not silently become user Annotations, canonical narrative objects, or facts.

## 2. Initial corpus scope

The V1 research corpus is deliberately small and limited to film/screenplay material. Only screenplay text is text-parsed in V1; a Film Source is a reference/metadata record, not an instruction to acquire or parse a film.

Build a set with variation, as rights and access permit, across:

- genre and genre combinations;
- period and production context;
- geography/culture where feasible and responsibly represented;
- narrative structure, pacing, chronology, viewpoint, and scene organization;
- screenplay formatting and source quality;
- familiar conventions and works that follow them;
- works that modify, invert, reject, or make conventions ambiguous;
- conventional and difficult cases, including missing/irregular scene headings, aliases, non-linear structure, and uncertain boundaries.

Select both representative cases and deliberately difficult cases. Difficult cases are not parser “noise” to discard; they expose assumptions and measure where the method fails.

Corpus selection principles describe how membership should be chosen. They do not name specific works. The inspected project documents do not identify a set of rights-cleared screenplay titles, so membership remains an open curation decision. Record the reason each Work was selected and which variation/difficulty it is intended to represent.

Do not claim a corpus is globally representative from a small pilot. Describe its selection frame and known gaps.

## 3. Work-level metadata

Work metadata identifies and describes a narrative work. Creator remains display metadata strings in V1; do not introduce a Creator entity or infer canonical creator identities.

| Field | Minimum meaning |
| --- | --- |
| work_id | Stable Work identity used by the shared Study / Make model. |
| title | Display title, preserving known alternate titles separately if required. |
| creator_display | One or more credited/display names as strings; role-specific authority records are not required in V1. |
| year | Known release/publication year or an explicitly unknown value; do not invent a date. |
| medium | Work medium, such as film/screenplay. A Work may have multiple Source representations. |
| language | Language of the relevant source/work where known. |
| genre | One or more descriptive metadata labels with provenance where curated; not a quality or formula label. |
| provenance | Catalog/source for the Work metadata and its curation. |
| source_availability | Whether a screenplay Source, Film Reference Source, both, or neither is available in this corpus context. |
| rights_governance_status | High-level status pointer to the more specific Source-level permissions and restrictions. |
| corpus_role | Why the Work is included (for example, pilot, variation case, difficult case, or held-out candidate). This is sampling intent, not a split assignment. |
| annotation_status | Summary of annotation coverage/review state; must not imply that unannotated narrative properties are absent. |

Creator display strings and Work metadata are not evidence for a claim about the narrative. A film and screenplay are Sources attached to a Work by default; distinct adaptations may be separate Works only by explicit editorial decision.

## 4. Source-level data

Source is the domain record that identifies a Work-linked source representation or reference. A stored/imported Document payload is an artifact behind Source, not a narrative entity.

| Field | Minimum meaning |
| --- | --- |
| source_id | Stable identity of this Work-linked source record. |
| work_id | Work to which this Source belongs. |
| source_kind | V1 values: screenplay or film_reference. |
| format | Format of the source payload/reference, such as plain text; record the actual value rather than implying broad parser support. |
| provenance | Provider/origin, attribution, known edition/publication details, acquisition/import context, and relevant dates. |
| source_revision_id | Immutable identity for the exact source content/reference revision used by locators and annotations. This is not the deferred Draft/Version entity. |
| original_content_ref | A controlled reference to the preserved original text payload or external film/metadata reference. |
| content_identity | Checksum/content digest where appropriate, with algorithm and exact bytes/text representation identified. |
| rights_governance | Separate known statuses/restrictions for storage, display/quotation, annotation, evaluation, and model-training/research use. |
| locator_strategy | Declared locator type, offset/index convention, line map, and source revision to which it applies. |

Only screenplay Sources are parsed as text in V1. A Film Reference Source may identify film metadata or a permitted external reference; it does not imply that the film itself is stored, displayed, or available for model processing. Source permissions are purpose-specific. Permission to annotate does not imply permission to publicly display or train on the content.

Preserve the exact original content. If a payload is replaced or changed, create a new source revision and preserve the old revision while referenced. Do not store parser output in place of the original. Rights metadata records known status and restrictions; it is not a legal conclusion.

## 5. Source locators

### Canonical locator

For parsed screenplay text, the canonical locator is a source-revision-scoped, half-open character span over the immutable decoded original text:

~~~text
source_id
source_revision_id
start_offset   inclusive
end_offset     exclusive
offset_unit    Unicode scalar-value index in decoded original text
~~~

The exact decoding policy and offset convention must be declared for each supported format. Preserve original bytes or an equivalently lossless payload, record its encoding/content identity, and make decoded text available unchanged for round-trip verification. Do not normalize Unicode composition or line endings in the canonical source string.

Line number and column are derived locators maintained by an index over the original text. Scene-local position is derived from the Scene's canonical source span. Page number is supplemental metadata only when it exists in the supplied original pagination; it is not a substitute for a stable text span. Film timestamps and image regions are later locator types.

### Mapping and round-trip rules

Every parser representation block, Scene span, Evidence span, and AnalysisClaim evidence link must preserve the chain:

~~~text
original source revision
→ parser representation and locator
→ narrative object or target
→ Evidence
→ AnalysisClaim
~~~

For each stored span, the system should be able to resolve the declared source revision, slice the original decoded text from start_offset to end_offset, and return the exact intended substring. Round-trip verification must fail visibly if the revision is missing or the span is out of bounds.

If processing normalizes line endings or otherwise creates a working text view, maintain an explicit reversible offset map from that derived view to the canonical original-text offsets. Never make a locator depend solely on rewritten, trimmed, or normalized text. Never repair a stale locator by silently searching for a similar string and moving it.

For accepted plain-text V1 inputs, preserve line numbers and offsets during parsing. If page numbers are unavailable in the original source, leave them unavailable instead of estimating them.

## 6. Corpus units

Not every unit below is a canonical object. The research layer must distinguish narrative identity, parser output, analysis, Evidence, and dataset labeling.

| Unit | Classification | Meaning / rule |
| --- | --- | --- |
| Work | Canonical narrative object | Shared narrative identity with descriptive metadata and one or more Sources. |
| Source | Canonical source object | Work-linked source representation/reference and revision/provenance boundary. |
| Scene | Canonical narrative object | Work-scoped narrative unit ordered in the Work and linked to a source span. |
| Block / ScriptBlock | Derived parser object | Classified screenplay text span such as scene_heading, action, character, dialogue, parenthetical, transition, or blank. It is not a Beat, Scene, Evidence, or claim. |
| Character | Canonical narrative object | Work-scoped participant; detection/cue candidates are not automatically canonical Character identities. |
| Event | Canonical narrative object | A thing that occurs in the story world, represented only with source support or explicit provenance. |
| Relationship | Canonical narrative object | A Work-scoped connection among Character participants. |
| Objective | Canonical narrative object | Something a Character is pursuing at a declared scope; a proposed label needs evidence and provenance. |
| Obstacle | Canonical narrative object | Something impeding an Objective; the link and obstacle type require evidence. |
| Information | Canonical narrative object | A knowledge item; introduction, knowledge, withholding, or change are separately supported claims/links. |
| Beat | Canonical narrative object | A small change unit within a Scene, curated or authored; not a formatting block. |
| Mechanism | Minimal canonical concept | V1 concept with id/name/description and explicit occurrence/claim links; no comprehensive taxonomy. |
| AnalysisClaim | Analysis object | A target-specific FACT, INFERENCE, or INTERPRETATION, linked to Evidence and provenance. |
| Evidence | Evidence object | A source revision and stable location supporting, challenging, or contextualizing a claim. |
| DatasetAnnotation | Research annotation record | A task-specific annotator judgment; it is not the product's user Annotation object or a new narrative entity. |

Do not create one canonical entity type for every label in an annotation task. For example, a “reversal candidate” may be a DatasetAnnotation or AnalysisClaim linked to a Scene and Mechanism, not a new universal Reversal object.

## 7. Annotation layers

Annotation layers describe different epistemic and authorship roles. Do not mix them into one free-form “analysis” field.

| Layer | What it records | Example | Rule |
| --- | --- | --- | --- |
| LAYER 1 — SOURCE OBSERVATION | Directly observable source details. | A character enters; a cue is followed by dialogue; a prop appears; the heading changes location; a line explicitly states a fact. | Narrow and verifiable against a source span. |
| LAYER 2 — STRUCTURAL / SEMANTIC LABEL | A derived label or relation supported by source evidence. | Objective, obstacle, Character/Relationship link, information event, reversal candidate, mechanism candidate, scene change. | Label the method/status; allow uncertain and no-match cases. |
| LAYER 3 — INTERPRETATION | A reasoned account of what a pattern may be doing. | A delayed reveal may redirect audience expectation. | Explicitly interpretive; alternatives may coexist. |
| LAYER 4 — COMPARATIVE RELATION | A relation between two or more source-grounded units. | Structural, relational, or formal similarity between two Scenes. | State the dimension and cite Evidence from every compared side. |
| LAYER 5 — USER MATERIAL | User-authored Notes and product Annotations. | A private question, observation, or tag anchored to a passage. | Preserve authorship and privacy; do not turn it into corpus truth by default. |

Research-layer DatasetAnnotations may label examples in Layers 1–4. They are annotation records for corpus work, not the product's user-generated Annotation entity in Layer 5.

## 8. FACT / INFERENCE / INTERPRETATION protocol

Every analytical claim must specify status, target, text/description, Evidence, provenance, author, and review state. An established AnalysisClaim requires one or more Evidence records. An unsupported hypothesis can remain an unaccepted proposal or a user Note, but it must not be represented as established analysis.

| Status | Protocol |
| --- | --- |
| FACT | Directly supported by an observable source span or explicit, provenance-backed metadata. State exactly what is present; do not smuggle intent or psychological meaning into the statement. |
| INFERENCE | Derived from observable evidence, but not stated literally. Identify the cues and the inference they support; qualify alternatives or uncertainty. |
| INTERPRETATION | A reasoned explanation of what an observed or inferred pattern may mean or accomplish. Keep it contestable and visibly separate from source fact. |

The same target may have more than one valid claim. Interpretations do not need to agree. A reviewer may accept multiple alternatives, reject one, or preserve the issue as unresolved. Confidence/certainty is optional and must only be recorded when the annotator can use a defined scale; it does not replace status or evidence.

## 9. Evidence protocol

Evidence qualifies when it points to a specific source revision and a verifiable source location that supports, challenges, or contextualizes the associated observation/claim. V1 screenplay research should prioritize exact text spans and line ranges. A Scene range is acceptable only when the claim concerns the whole Scene and the relevant supporting passages remain locatable within it.

For each Evidence record preserve:

- source_id and source_revision_id;
- canonical start/end span and derived line range;
- the relation to the associated claim (supports, challenges, or context);
- a concise observation or explanation of relevance;
- excerpt text only when rights/governance permit storing or displaying it;
- provenance of any curator/reviewer who selected it.

Future media may add film timestamps or image regions, each with a medium-specific locator. They do not replace screenplay text spans in the initial research task.

Insufficient evidence includes:

- “this feels important” without a source span or a reasoned, labeled interpretation;
- “the protagonist is insecure” without source details supporting that psychological inference;
- “the director wants us to…” without source support or attributable contextual evidence;
- a scene label with no cited span;
- a quotation from a different Source revision;
- a broad claim whose cited line is merely adjacent to, but does not support, the claim.

These statements may be recorded as hypotheses or interpretations if qualified and tied to relevant evidence. They may not be presented as source-grounded FACTs. If evidence is insufficient, record that state explicitly and abstain from making an established claim.

## 10. Dataset annotation record

The research annotation record is named DatasetAnnotation here to distinguish it from the product's user-generated Annotation object. DatasetAnnotation is a protocol judgment; it is not itself a narrative object, Evidence, or an AnalysisClaim.

| Field | Meaning |
| --- | --- |
| annotation_id | Stable identity for this annotator's judgment/version. |
| task_id / layer | Annotation task and epistemic layer being labeled. |
| source_id / source_revision_id | Exact Work source revision considered. |
| annotator | Annotator identity or governed pseudonymous ID and relevant protocol/training version. |
| target | One or more target references, such as Work, Scene, Character, span, or Scene pair. |
| label | Chosen task label, including explicit ambiguous, insufficient-evidence, abstain, or no-match values where allowed. |
| text / description | Narrow annotation content or rationale. |
| evidence_refs | One or more stable Evidence/source-span references; required for source-grounded claims. |
| status | FACT, INFERENCE, or INTERPRETATION when the record expresses an analytical claim. |
| certainty / qualification | Optional qualification using a defined scale or controlled wording; never an unexplained numeric score. |
| alternatives | Other plausible labels/claims, with separate evidence and rationale where available. |
| comments | Annotator notes, protocol questions, or reasons for abstention. |
| review_state | Unreviewed, second-reviewed, adjudicated, rejected, or other documented workflow state. |
| created_at / protocol_version | Provenance for when and under which annotation guidance the record was made. |

Keep separate DatasetAnnotation records for independent annotators. Do not overwrite the first judgment with an adjudicated result; retain the lineage and reviewer decision.

## 11. Inter-annotator disagreement

Represent disagreement as data, not as a defect that must be erased. At minimum, the review state for an annotation set may include:

- agreement;
- disagreement;
- unresolved;
- ambiguous;
- insufficient evidence;
- abstain.

These are review outcomes, not narrative entities or forced truth labels. Store the underlying annotator records and their rationales; attach agreement/disagreement status to the set of judgments for a target/task. Where appropriate, preserve multiple valid interpretations as separate AnalysisClaims with separate Evidence.

Example:

~~~text
ANNOTATOR A
Objective: persuade Mark to leave.
Evidence: cited line/action spans.

ANNOTATOR B
Objective: test whether Mark will stay.
Evidence: cited line/action spans.

REVIEW OUTCOME
Disagreement / alternative interpretations retained.
~~~

Do not collapse this into one forced objective merely because a classifier expects a single label. Adjudication may choose a task-specific reference answer, but must retain the original judgments and explain the decision. Disagreement can be used to test ambiguity handling, calibration, abstention, and whether a model overstates certainty.

## 12. Negative and counterexample data

Every task must include examples beyond positive instances:

- **Positive examples:** the label is supported by the source under the protocol.
- **Negative examples:** the relevant label is not supported, even if a surface cue is present.
- **Ambiguous examples:** more than one label or interpretation is defensible.
- **Counterexamples:** a tempting generalization fails in this case.
- **Convention-breaking examples:** the Work modifies, inverts, rejects, or avoids a familiar convention.
- **No-match cases:** the candidate set contains no supported label or relation.

For a reversal task, include Scenes with tension, surprise, or a new fact that are not reversals under the written definition. Include scenes that create change in ways not represented by the initial mechanism vocabulary. Otherwise the dataset teaches a model to force a label whenever it sees a dramatic cue.

Negative examples are not “bad stories.” They are examples that prevent a method from confusing correlated surface features with the target concept.

## 13. Mechanism annotation

Use the minimal V1 Mechanism vocabulary from the intelligence architecture. Initial candidate labels may include:

- objective;
- obstacle;
- confrontation;
- information reveal;
- information withholding;
- reversal;
- preparation;
- aftermath;
- transition.

These are descriptive candidates, not a complete taxonomy or a required checklist for every Scene.

For each proposed occurrence, capture:

- mechanism concept or candidate label;
- target Scene and Work;
- source revision and Evidence spans;
- DatasetAnnotation / annotator identity;
- concise rationale for why the label applies;
- alternatives or overlapping mechanisms;
- qualification and review status;
- explicit abstain/no-match where appropriate.

Do not assign a Mechanism to every Scene. Keep an unclassified/no-match result valid. Track the Mechanism concept separately from its occurrence in a particular Scene; do not create a separate canonical entity for each occurrence.

## 14. Objective / Obstacle annotation

### Objective protocol

For an Objective candidate, record:

1. **Whose objective?** Link to a Work-scoped Character, or mark unknown/collective where supported.
2. **What appears to be pursued?** Phrase narrowly as an action or desired result.
3. **At what scope?** Scene, beat, sequence, or broader Work-level pursuit; do not infer scope from screen time alone.
4. **How explicit is it?** Directly stated, behaviorally inferred, contested, or not determinable.
5. **What supports it?** Attach spans showing the stated desire, action, response, or decision.
6. **What alternatives exist?** Preserve plausible competing objectives and rationale.

Avoid claims about hidden psychology unless the source gives evidence. “She wants the key” may be explicit; “she fears intimacy” is an interpretation/inference requiring different, sufficient support and qualification.

### Obstacle protocol

For an Obstacle candidate, record:

- which Objective is impeded;
- what prevents or complicates it;
- obstacle category, if useful: another Character, environment, information, internal contradiction, time, institution, or other;
- whether the obstacle is explicit or inferred;
- the source spans showing the attempt and impediment;
- effect/outcome only where supported;
- alternatives and uncertainty.

Do not assume every Objective has one discrete Obstacle, or that conflict must appear in every Scene. A category such as “internal” must be supported by the source and should not become an unsupported diagnosis.

## 15. Information annotation

An Information annotation concerns a defined knowledge item and a supported event/relation involving a Character or audience. Candidate labels:

- information introduced;
- information discovered;
- information revealed;
- information withheld;
- information misunderstood;
- asymmetric knowledge.

For each record ask:

~~~text
WHO KNOWS WHAT?
WHEN?
HOW DOES KNOWLEDGE CHANGE?
~~~

Record the Information item, relevant Characters/audience when supported, when it is introduced/discovered/revealed/withheld, and Evidence spans. Distinguish the text that states or signals the item from an inference about who understands it. “Not shown to know” is not automatically “does not know.” Preserve uncertainty and contradictory evidence.

Do not infer a complete knowledge state from one line or from current untyped Scene state dictionaries. Full knowledge timelines and setup/payoff tracing remain later research.

## 16. Character / Relationship annotation

- **Character:** identity of a participant within one Work. V1 does not attempt identity across Works.
- **Appearance:** a Character's participation or presence in a Scene, linked to accepted cue/source spans. A cue is evidence of a screenplay label, not necessarily proof of an underlying character identity in every case.
- **Relationship:** a Work-scoped connection between two or more Characters. Record participants and any supported descriptive relation with Evidence.
- **Relationship change:** a claim about a supported difference between scenes/states, with source spans from relevant points. It may remain contested or not measurable.

Do not infer personality traits simply from role labels, name capitalization, genre expectations, or dialogue tone. Distinguish an observable action/utterance, an inference about a relationship, and an interpretation of its meaning. Do not attempt cross-Work identity in V1. Do not present numeric trust, power, attraction, or hostility values as objective measurements without a defined scale and evidence protocol.

## 17. Event annotation

Keep these units distinct:

| Unit | Definition |
| --- | --- |
| Scene | A screenplay/narrative unit, represented by a Work-scoped object and a source span. |
| Beat | A smaller interaction/change unit within a Scene. It is a narrative change unit, not a line or parser block. |
| Event | A thing that occurs in the story/narrative world, with participants/time/location/causal links where known. |

A Scene may contain one or more Events, and an Event may be represented across more than one Scene or occur off-screen. These links need explicit evidence/provenance. Parser formatting does not establish an Event or Beat automatically. A transition, heading, or dialogue exchange may be evidence for a curator's record but does not itself determine narrative significance.

Events represented as explicit narrative facts require source support or an identified, governed source for off-screen/backstory information. Separate chronology from causality; temporal order alone does not prove cause.

## 18. Structural similarity dataset

Create future similarity data as explicit pair/group judgments, not one undifferentiated scalar. Label dimensions separately:

- surface similarity;
- structural similarity;
- relational similarity;
- formal similarity;
- historical influence.

For each pair/group record:

- pair/group ID and target Works/Scenes;
- relation type and dimension-specific label;
- explanation of what corresponds and what differs;
- Evidence from each side, anchored to its own Source revision;
- annotator and review state;
- confidence/qualification only under a defined protocol;
- disagreement, alternatives, and difficult-negative status.

Historical influence is not established by structural or surface similarity. It needs separately attributable historical/contextual evidence. Include difficult negative pairs with shared setting, words, genre, or event but no relevant structural relation. For cross-Work retrieval, evaluate whether the explanation faithfully covers both items and whether it distinguishes the requested dimension.

## 19. Transformation data

Transformation data is future research only and is not part of V1 implementation or the initial annotation task. A future controlled record may:

~~~text
SOURCE SCENE
→ identify a supported structural mechanism
→ change setting / characters / era
→ preserve or alter relationships
→ record the transformed scene and lineage
→ evaluate what appears structurally invariant or changed
~~~

Store the original source and transformed output as separate, linked artifacts with explicit user authorship and lineage. Do not treat transformed text as source evidence for the original Work. Evaluate whether the proposed invariant is supported; do not use transformation to prove a universal screenplay rule.

## 20. Train / validation / test splits

Prefer splitting by Work rather than randomly splitting Scenes. Scenes from the same Work share characters, style, events, and plot context; splitting them across train and evaluation can make memorization look like generalization.

Maintain disjoint groups:

- **Train Works:** records allowed for fitting a task model or training a specialized component.
- **Validation Works:** records used for model selection, prompt/rubric iteration, or threshold selection.
- **Held-out test Works:** sealed records used for final evaluation only.

For cross-Work retrieval, hold out entire Works from query and/or candidate roles according to the research question; document whether a held-out Work is excluded from the retrieval index. Group related source revisions, screenplay/film representations, adaptations, and closely linked Works to reduce leakage where the evaluation goal requires unseen narrative material.

Keep test annotations and outputs out of training, prompt examples, retrieval stores used during development, and post-hoc model improvement. If a test result leads to a method change, that test set is no longer an untouched final test for the changed method; use a new held-out set or clearly label the evaluation exploratory.

Foundation models may have seen public works during pretraining. Record that as a limitation; do not claim that a Work-level split eliminates pretraining exposure. Test whether task performance depends on memorized title-specific knowledge by using source-grounded questions, unseen/less-known Works where rights allow, and evidence checks.

## 21. Gold dataset governance

| Tier | Definition | Permitted use |
| --- | --- | --- |
| GOLD | Human-reviewed annotation under a versioned protocol; independently reviewed and adjudicated where needed. Legitimate alternatives can all be Gold when the protocol supports them. | Formal evaluation for the defined task/split; training only if the split and governance explicitly permit it. |
| SILVER | Model-assisted or single-reviewer labels not yet fully validated, with provenance retained. | Development, triage, or exploratory analysis; not formal test truth. |
| UNREVIEWED | Candidate annotations or raw model proposals awaiting review. | Review queue only; not gold evaluation or training truth by default. |

Only clearly defined, rights/governance-cleared subsets may be used for formal evaluation. A plausible-looking model output is not Gold. Tier changes require review provenance and must not erase the former tier or label history. Gold data may preserve multiple valid interpretations and disagreement rather than forcing a single answer.

## 22. Human annotation workflow

~~~text
SELECT SOURCE
→ REVIEW SOURCE
→ CREATE DATASET ANNOTATION
→ ATTACH EVIDENCE
→ ADD ALTERNATIVES
→ SECOND REVIEW
→ ADJUDICATE IF NEEDED
→ GOLD / SILVER / REJECT
~~~

Annotators can abstain or mark insufficient evidence. A second reviewer assesses the label and its evidence, not merely whether the text sounds plausible. Adjudication records the reason for a decision and retains original judgments. Rejected examples and reasons may be valuable negative data if rights/governance permit their use.

Measure annotation quality separately from model quality. Report annotator agreement, evidence sufficiency, protocol ambiguity, and adjudication rate independently of model precision/recall or response usefulness.

## 23. Annotation guidelines

1. Annotate only what the source supports.
2. Separate observation from inference and interpretation.
3. Cite a stable source span for every source-grounded claim.
4. Preserve ambiguity, contradiction, and alternative readings.
5. Do not infer unsupported psychology or intent.
6. Do not force a category when “unclear,” “other,” or “no match” is more faithful.
7. Record alternative interpretations and their evidence.
8. Prefer narrow, local claims over sweeping claims about a whole Work.
9. Preserve source wording and locators; do not anchor against rewritten text.
10. Keep annotator, source revision, protocol version, and review state.
11. Do not use the task to impose textbook formulas or expectations.
12. Do not treat a user Note/Annotation, parser guess, or model proposal as corpus fact without the appropriate review and provenance.

## 24. Dataset tasks

These are research task definitions, not decisions to deploy models. A task target is evaluated against protocol labels and source evidence.

| Task | Input | Target | Annotation source | Evaluation metric | Human review requirement | Likely baseline |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Scene segmentation | Screenplay text and parser blocks | Scene boundaries and source spans | Double-reviewed boundary set | Boundary precision/recall and span alignment | Review uncertain/malformed boundaries | Existing heading rules / regex parser |
| 2. Character cue normalization | Character cue blocks within a Work | Normalized cue groups, preserving raw forms | Annotator-reviewed aliases | Pairwise linking precision/recall; false merge rate | Review merges and splits | Exact string normalization and rules |
| 3. Character identity linking within Work | Accepted cues, scene spans, dialogue/action context | Cue/appearance links to Work-scoped Characters | Gold identity links with ambiguous cases | Link precision/recall and abstention quality | Review identity candidates | Deterministic cue grouping |
| 4. Objective candidate extraction | Scene text, representation, relevant Characters | Candidate Objective, target Character, scope, evidence | Human-reviewed objective labels | Precision/recall, evidence sufficiency, unsupported rate | Required for accepted claims | Keyword/rule and direct LLM prompt baselines |
| 5. Obstacle candidate extraction | Objective candidates and Scene source spans | Candidate Obstacle, type, affected Objective, evidence | Human-reviewed obstacle labels | Precision/recall by type; unsupported claim rate | Required | Rules plus direct LLM prompt |
| 6. Information event extraction | Scene sequence, Character links, source spans | Introduced/discovered/revealed/withheld/misunderstood/asymmetric labels | Reviewed Information annotations with alternatives | Label precision/recall, status accuracy, evidence sufficiency | Required; disagreement retained | Keyword retrieval and direct LLM prompt |
| 7. Mechanism candidate retrieval | Scene text/claims and small curated vocabulary | Candidate Mechanism occurrences or no-match | Gold/Silver mechanism examples and negatives | Precision/recall, false-positive rate, human relevance | Required for corpus use | Keyword/BM25 and embedding retrieval |
| 8. Evidence span retrieval | Claim/question and source representation | Supporting source span(s) | Gold span links | Exact/partial span match, evidence sufficiency | Review unsupported and partial matches | Keyword/BM25 |
| 9. Claim status classification | Claim text plus cited source context | FACT / INFERENCE / INTERPRETATION / abstain where applicable | Adjudicated status labels including disagreements | Status accuracy, per-class metrics, unsupported claim rate | Required on uncertain cases | Rubric rules and direct LLM prompt |
| 10. Structural similarity retrieval | Query Scene/claim and candidate corpus | Ranked Scene pairs by declared dimensions | Reviewed pair labels and difficult negatives | Recall@k, human relevance, explanation faithfulness | Human evaluation required | Metadata, BM25, and embedding retrieval |

Choose metrics and label granularity before inspecting held-out test output. A task may prove unsuitable for automation; documenting that result is a valid research outcome.

## 25. Baselines

Every advanced method is compared against a meaningful, reproducible baseline using the same task split and source access:

- **Regex/rule-based parser:** current screenplay heading, transition, cue, parenthetical, dialogue, action, and blank-line heuristics; measure its actual limits.
- **Metadata search:** deterministic title/creator/year/genre/medium filters where metadata exists.
- **Keyword retrieval:** exact or normalized term matching for source spans.
- **BM25/text retrieval:** lexical ranking over screenplay spans or descriptions.
- **Embedding retrieval:** semantic candidate ranking; evaluate against lexical and human judgments, not just similarity scores.
- **Direct LLM prompt without structured context:** a comparison baseline for the value of retrieval, source locators, and structured tools; require the same source material and judge grounding separately.

Keep the retrieval corpus, prompts, model versions, and indexes fixed/documented for each comparison. A more complex method should demonstrate benefit on the target task, not only produce more elaborate prose.

## 26. Dataset size strategy

Do not invent a screenplay count target such as “10,000 screenplays.” Increase scope only when annotation quality and task utility justify it.

1. **SMALL PILOT:** enough rights-cleared, varied material to test source alignment and whether annotators can apply the protocol consistently. Depth and error review matter more than count.
2. **MEDIUM GOLD SET:** add Work-level variety and difficult/negative cases until task-specific evaluation is stable enough to compare initial methods. Determine adequacy from confidence intervals, class coverage, and observed error diversity rather than a fixed arbitrary count.
3. **LARGER CORPUS:** expand only after governance, annotation agreement/disagreement handling, and measurable task value have been demonstrated.

Use a stratified/deep-slice approach: deeply annotate selected Works and selected Scenes, while preserving broader source/metadata coverage where permitted. Do not pretend sparse annotation is complete coverage.

## 27. Evaluation metrics

Use metrics suited to the task and report them by relevant strata (format, genre/structure, ambiguity, and source quality) where the sample permits.

| Metric | Use |
| --- | --- |
| Scene boundary precision / recall / F1 | Evaluate proposed boundary locations against reviewed boundary spans under a declared matching tolerance. |
| Character linking precision / recall | Evaluate cue-to-Character links; report false merges separately from missed links. |
| Evidence span exact match | Strictly measure whether predicted start/end equal the reference span. |
| Evidence span partial match | Measure overlap/coverage using a declared overlap rule; do not treat a partial hit as fully sufficient automatically. |
| Claim status accuracy | Evaluate FACT/INFERENCE/INTERPRETATION labels, per class and on ambiguous/disputed cases. |
| Unsupported claim rate | Fraction of surfaced claims whose cited evidence fails to support the claim under review. |
| Abstention quality | Measure appropriate abstention on insufficient/ambiguous cases and avoid rewarding abstention on easy supported cases. |
| Retrieval recall@k | Fraction of known relevant candidate items present among the top k, for a defined relation dimension. |
| Human relevance rating | Blinded rating of candidate usefulness/relevance under a written rubric; report agreement and distribution. |
| Explanation faithfulness | Whether the explanation accurately represents both source items and the labeled comparison. |
| Inter-annotator agreement | Agreement by task/label, paired with disagreement and ambiguity analysis; choose a statistic suited to nominal/ordinal/multi-label data rather than one universal score. |
| False-positive rate | Especially important for forced mechanisms, psychological labels, and similarity retrieval. |

Fluency is not a metric for narrative understanding. Fluency may be assessed as a presentation quality after source faithfulness and task correctness are measured; it cannot substitute for them.

## 28. Model-improvement loop

~~~text
MODEL / METHOD
→ PROPOSE
→ RETRIEVE EVIDENCE
→ HUMAN REVIEW
→ CORRECT / REJECT / ABSTAIN
→ APPROVED DATA WITH PROVENANCE
→ HELD-OUT EVALUATION
→ CONTROLLED MODEL / METHOD CHANGE
~~~

Do not allow uncontrolled self-training. Raw model output, model self-approval, or repeated copies of model-generated labels do not become Gold. A corrected proposal can become a training candidate only after human review, rights/governance checks, and split assignment that excludes held-out evaluation Works.

Every method change should be evaluated against a stable baseline and untouched test data. Once held-out labels or outputs influence training, prompts, thresholds, or retrieval design, mark that set as development data and reserve a new test set for a final claim.

## 29. Corpus rights and governance

Track rights and governance at the Source and, where necessary, payload/span level:

- provenance and source attribution;
- copyright/usage status as known;
- permission/status to store;
- permission/status to display or quote;
- permission/status for internal research;
- permission/status for annotation and evaluation;
- permission/status for model training or other reuse;
- access, retention, and deletion restrictions;
- public-display eligibility separate from internal research eligibility;
- review owner, status date, and supporting permission record/reference.

Before adding a source, a responsible curator records provenance and checks the applicable use scope. If status is unknown or incompatible with the intended use, do not ingest or expose the material for that use. Keep internal research and public Story Atlas eligibility distinct.

This is a traceability and governance requirement, not legal advice. No source is presumed cleared because it is accessible online or because a user supplied it.

## 30. Visual-art extension

Visual-art annotation is a separate future protocol. Do not force a painting into screenplay Scene/Beat structures. Use image-specific regions and media-appropriate object/relation labels.

Potential layers:

- **OBSERVATION:** object, figure, spatial relation, gesture, gaze, composition, color, shape.
- **INFERENCE:** candidate relation/function inferred from observed visual details.
- **INTERPRETATION:** symbolic, thematic, or contextual explanation.
- **EVIDENCE:** image region, with image/version identity and region locator.
- **ALTERNATIVES:** other plausible readings, disagreements, and limits.

A visual observation such as “two figures occupy opposite sides of the composition” must remain distinct from an inference that separation is significant and an interpretation that it expresses alienation. Cite the image region and provenance; do not assert symbolic meaning as direct observation. All visual-art data, models, and experiments remain future research.

## 31. First corpus build

The first research workflow should be a deep, bounded pilot:

1. Curate a small number of screenplay Sources whose intended storage and research use are governed and documented.
2. Preserve original revisions and manually verify source alignment and round-trip locators.
3. Apply scene segmentation and inspect both ordinary and difficult formatting cases.
4. Normalize character cues and link identities within each Work, retaining uncertain/ambiguous cases.
5. Add narrow Objective, Obstacle, and Information labels to selected Scenes with Evidence.
6. Annotate Mechanisms only for selected scenes; include negative/no-match cases.
7. Have a second annotator review a subset and retain disagreements.
8. Hold out complete Works for task evaluation before any model-assisted development.
9. Report protocol failures and source/rights gaps before expanding the corpus.

Do not require every Work to be deeply annotated immediately. Use a stratified/deep-slice design: deeply annotate selected Works and Scenes, while recording the intended coverage and unannotated areas. This document identifies no specific cleared screenplay titles; selecting membership is a separate governed curation decision.

## 32. What becomes training data

### Good candidates for training, subject to governance and split policy

- human-reviewed scene boundaries and source spans;
- reviewed character cue normalization and within-Work identity links;
- evidence-grounded Objective and Obstacle labels;
- Information events and knowledge-change labels with alternatives;
- reviewed Mechanism occurrences and no-match cases;
- structural similarity pairs with dimension-specific explanations;
- accepted or rejected model proposals when the human decision, rationale, provenance, and source Evidence are retained.

Training use is task-specific. Acceptance as a valid corpus annotation does not automatically grant permission for model training. Exclude validation/test Works from training, prompt examples, and tuning.

### Not training truth by default

- raw model output;
- unsupported interpretations;
- private user Notes or user Annotations;
- speculative/unreviewed annotations;
- unresolved disagreements treated as single facts;
- labels whose source, annotator, or protocol provenance is missing.

User-generated material remains separate unless the user explicitly consents and the use is governed. Consent for one use does not imply consent for another.

## 33. What becomes evaluation data

Create a held-out evaluation set with:

- unseen Works;
- difficult scenes and formatting;
- ambiguous cases;
- convention-breaking examples;
- negative and counterexamples;
- no-match cases;
- competing interpretations and legitimate disagreement;
- source spans needed to verify each target.

Evaluation Works and labels remain isolated from training and development. For cross-Work retrieval, clearly define whether held-out Works are excluded from queries, candidate indexes, or both. Do not use test outputs to create training labels. Keep a record of each evaluation set version and every access that could affect its independence.

## 34. Success criteria for the corpus

The corpus design is successful when:

1. The original source revision can be reconstructed and source spans round-trip exactly.
2. An analyst can trace each established claim to source Evidence and provenance.
3. Multiple interpretations can coexist without forced consensus.
4. Annotation disagreement, ambiguity, insufficient evidence, and abstention are visible.
5. Training, validation, and held-out evaluation data are separated by Work and governed.
6. Model-generated labels are never mistaken for truth solely because they sound plausible.
7. The dataset captures narrative variation, difficult examples, and counterexamples rather than only textbook patterns.
8. The corpus is useful for evaluating actual Narrative Lab capabilities, including failure and no-match behavior.
9. Rights and access eligibility are known for each intended corpus use.

## 35. Important boundary

Narrative Lab is not building a model that predicts the “correct” screenplay structure.

It is building a system that can:

- represent what narrative works do;
- locate evidence;
- identify recurring patterns;
- distinguish variations;
- compare structures;
- preserve uncertainty;
- support human interpretation.

The corpus must therefore include works that follow conventions, modify conventions, invert conventions, reject conventions, create ambiguity, and resist simple categorization. Do not collapse descriptive pattern discovery into prescriptive storytelling rules.

## 36. Final deliverable

### NARRATIVE CORPUS V1

~~~text
SOURCE CORPUS
└── WORK
    └── SOURCE (screenplay text or film reference)
        └── immutable source revision
            └── SOURCE REPRESENTATION
                ├── parser BLOCKS (derived, source-aligned)
                └── SCENES (canonical, source-spanned)
                    ├── CHARACTER / APPEARANCE
                    ├── RELATIONSHIP
                    ├── EVENT
                    ├── OBJECTIVE / OBSTACLE
                    ├── INFORMATION
                    └── BEAT / MECHANISM (curated, not inferred from formatting)
                        └── ANALYSIS CLAIM
                            └── EVIDENCE (source revision + exact locator)
                                └── REVIEW STATUS / PROVENANCE
~~~

The hierarchy is conceptual. Relationships can be many-to-many; the tree does not prescribe database tables or imply that every Work contains every annotation category.

### ANNOTATION TASKS V1

1. Scene segmentation.
2. Character cue normalization.
3. Character identity linking within one Work.
4. Objective candidate annotation.
5. Obstacle candidate annotation.
6. Information event annotation.
7. Mechanism candidate retrieval/annotation on selected Scenes.
8. Evidence span retrieval/alignment.
9. Claim status classification.
10. Structural similarity retrieval with separate relation dimensions.

### TRAINING DATA

Only task-appropriate, rights/governance-cleared, human-reviewed labels with preserved Evidence and provenance; accepted/rejected proposals only with review rationale; no validation/test Work leakage. Raw model output and private user material are excluded by default.

### EVALUATION DATA

Work-disjoint held-out Gold subsets containing unseen and difficult Works, ambiguity, disagreement, negative examples, counterexamples, no-match cases, and source-linked Evidence. Keep them isolated from prompt, retrieval, and training data used for model development.

### DEFERRED DATA

Large-scale all-media corpus; film-video transcript/visual ingestion; film timestamps; visual-art regions; cross-media equivalence; comprehensive Narrative State, Theme/Motif/Setup/Payoff/Convention taxonomies; transformation outputs; cross-Work Character identity; Draft/Version histories; autonomous interpretation; broad historical-influence labels.

### FIRST PILOT EXPERIMENT

Select a small, varied set of screenplay Sources only after rights/governance review. Preserve exact source revisions; manually verify locators; annotate Scene boundaries and within-Work Character links; deeply label a subset for Objective, Obstacle, Information, and selected Mechanisms with source Evidence; include ambiguity, negatives, and no-match cases; obtain independent review; hold out complete Works; compare rule-based/lexical baselines with model-assisted proposals only after the protocol is stable.

Success means the source round-trips, claims are traceable, disagreement remains visible, and the pilot can measure where methods fail. It does not require a predetermined number of screenplays or a training run.

### OPEN RESEARCH QUESTIONS

- Which screenplay text formats can the pilot support while preserving exact source positions?
- Should a changed source payload create a new Source or a new revision under the same Source ID?
- What locator decoding/index convention best supports exact round-trip behavior across the chosen toolchain?
- Which rights-cleared sources provide meaningful variation without overstating representativeness?
- What annotation protocol yields reliable local claims while preserving interpretive disagreement?
- Which claims are appropriate for FACT versus INFERENCE when source conventions are ambiguous?
- What evidence-span granularity is sufficient for objectives, obstacles, and information changes?
- Which task-specific agreement and acceptance thresholds are justified by the pilot data?
- Do model-assisted methods improve on deterministic, lexical, or human-curated baselines for each task?
- How should held-out retrieval candidates be isolated when evaluating cross-Work similarity?
- Which model tasks, if any, merit later specialization, and what uses are permitted by source governance?
- Which high-level concepts can be shared across media without flattening screenplay, film, and visual-art representations?
