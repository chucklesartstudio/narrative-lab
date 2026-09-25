# Narrative Intelligence Architecture

## Purpose and status

This is a future-facing architecture and research specification for how Narrative Lab may represent, analyze, retrieve, compare, and reason about narrative works. It builds on the repository's narrative model, product maps, and architecture decisions; it does not replace them.

This document specifies no application code, UI, API, model dependency, training run, or database implementation. It distinguishes the proposed V1 object model from later intelligence capabilities and experiments. A capability described here is not thereby a V1 product commitment.

Source documents:

- [Narrative model](narrative-model.md) — existing conceptual narrative vocabulary and fact/inference/interpretation principle.
- [Architecture decisions](../product/narrative-lab-architecture-decisions.md) — proposed V1 object classifications and relationship boundaries.
- [Feature map](../product/narrative-lab-feature-map.md) and [screen map](../product/narrative-lab-screen-map.md) — Study and Make workflows, evidence and source requirements, and future roadmap.
- [Studio-derived system](../design/studio-derived-system.md) and [Studio feature inventory](../design/studio-feature-inventory.md) — presentation and interaction patterns only; the Studio prototype is not the narrative ontology or an implementation reference for intelligence.

The proposal follows the architecture decisions' defaults: one Work may have Film and Screenplay Sources; Source is a V1 domain object and a stored document is its payload; Creator remains Work metadata; Notes and Annotations are separate user-generated objects; typed Structural Unit and Narrative State objects are deferred; Library is the personal Reference Shelf destination. These are architectural defaults from the companion decisions document, not silent edits to the earlier ontology or an implemented schema.

## 1. Product principle and boundaries

Narrative Lab is a narrative intelligence system with a user-facing research and writing environment. It is not primarily a chatbot.

The initial medium is film and screenplay. The system should help people study existing works, inspect scenes and characters, trace evidence and information, identify narrative mechanisms, compare material, and develop their own writing using shared narrative objects. Visual art and other media are later extensions.

The governing principle is descriptive:

> Narrative Lab should learn from what works have actually done. It must not turn recurring patterns into rules about what stories are supposed to do.

The system must preserve variation, ambiguity, contradiction, unconventional structure, and legitimate alternative interpretations. A model output can be useful without being definitive. A fluent answer is not proof that the system understood the work.

The shared Study / Make model means that the same Work, Scene, Character, and other canonical objects can appear in both contexts. It does not make user material public or make a private Note a source fact. Ownership, rights, and provenance remain explicit.

### Scope labels used here

- **V1 object** means a canonical object or relation required by the proposed V1 product model. It does not imply that its backend schema is already implemented.
- **V1 analysis** means a bounded, inspectable deterministic or human-curated result needed to support the initial Study / Make loop.
- **Research capability** means a capability to validate through experiments before productizing.
- **Later concept** means a concept intentionally deferred by the architecture decisions, such as a typed Structural Unit, Draft, or Version entity.

## 2. Central architecture

~~~text
SOURCE
  → INGESTION
  → REPRESENTATION
  → STRUCTURAL ANALYSIS
  → EVIDENCE / CLAIMS
  → RETRIEVAL / COMPARISON
  → MODEL REASONING
  → USER INTERACTION
~~~

The layers have different responsibilities. Provenance, rights, and human review cross the layers; they do not replace the layer boundaries.

| Layer | Responsibility | Output and boundary |
| --- | --- | --- |
| Source | Identify and preserve the original material and its provenance. | A Work-linked Source and its original payload or external reference. Parser output is never the original. |
| Ingestion | Safely receive, identify, validate, and prepare a source for processing. | A source revision identity, format information, intake status, and reproducible processing input. It does not decide what a story means. |
| Representation | Describe observable source structure and canonical narrative objects. | Source-aligned ScriptBlocks, scene boundaries, character cues/appearances, and curated canonical records. Representation may include uncertainty; it is not interpretation. |
| Structural analysis | Calculate inspectable properties and relations from the representation. | Counts, ordering, durations or lengths in declared units, co-occurrence, and other reproducible measures. These describe patterns and do not prescribe a formula. |
| Evidence / claims | Preserve what supports an analytical statement and label the statement's epistemic status. | Evidence points to a stable source location. AnalysisClaim states FACT, INFERENCE, or INTERPRETATION and links its target, support, and provenance. |
| Retrieval / comparison | Find relevant Works, scenes, claims, and evidence; compare them under explicit criteria. | Ranked or filtered candidates with reasons and source links. Similarity is not proof of influence or equivalence. |
| Model reasoning | Use retrieved, structured context and tools to produce a bounded explanation or proposal. | A sourced, status-labeled claim or response, with abstention where support is inadequate. No monolithic model owns the truth. |
| User interaction | Let a person inspect sources, navigate linked objects, review claims, and create their own material. | Contextual views over shared objects; private Notes and anchored Annotations remain distinct from corpus claims. The UI does not change object identity. |

### Concepts that must stay separate

| Concept | Meaning |
| --- | --- |
| SOURCE | The original screenplay text or the identity/reference for a film or other work material. |
| REPRESENTATION | A structured description of observable source content, such as classified screenplay blocks and source-aligned scene spans. |
| ANALYSIS | Derived properties or claims about a representation. Analysis may be calculated, curated, or model-assisted. |
| EVIDENCE | A source excerpt or location that supports, challenges, or contextualizes a claim. Evidence is not the claim itself. |
| INTERPRETATION | A reasoned explanation of what an observed or inferred pattern may be doing. It is a claim status, not a source fact. |
| USER MATERIAL | Private or user-authored Notes and Annotations. It may refer to evidence, but does not become evidence or a corpus claim automatically. |

## 3. Source layer

### Work and Source

The canonical relation is:

~~~text
Work
  └── has one or more Sources
~~~

A Work is the narrative-level identity used in Study and Make. A Source identifies a particular representation or reference used to study that Work. For the initial medium, the Source kinds are:

- **Screenplay text** — original text supplied or curated for parsing and source-span navigation.
- **Film reference / metadata** — an identifier or reference to a film and the metadata/provenance needed to identify it. A film reference does not imply that Narrative Lab stores or has rights to the film itself.

By default, a film and its screenplay are separate Sources for one Work. Treat an adaptation as a separate Work only when an explicit editorial decision considers it a distinct narrative work; do not infer this from format or file type. Preserve the ability to link related Work records later without requiring a V1 adaptation graph.

### Source identity and source version

A Source needs a stable identity within a Work and a clear identity for the specific content revision to which locations refer. Replacing screenplay text must not silently change the meaning of existing line or character-offset anchors.

The V1 boundary is:

- Source identity and provenance are required.
- An imported source payload should be treated as an immutable snapshot for the lifetime of its evidence and annotations.
- Re-imported or materially changed content receives a new source revision identity, or a new Source identity if the product elects that narrower policy.
- The existing Work.version string remains descriptive metadata. It is not version history.
- A separate Draft or Version entity is deferred. A source revision identifier is necessary for reproducible locators but does not itself require a Version domain entity.

The product must decide whether a changed payload creates a new Source or a revision under the same Source before source replacement is implemented. Either policy must preserve the old payload identity when existing evidence references it.

### Source record responsibilities

The Source domain record should be able to resolve or point to:

- stable Source ID and owning Work ID;
- source kind, medium, and format (for example, screenplay text and its accepted import format);
- original payload identity or external film/reference identifier;
- source revision identity or content digest sufficient to detect changed text;
- provenance such as supplied-by/credited source, publisher or origin, source date when known, and acquisition/import context;
- stable locator scheme and the revision to which its locators apply;
- access and rights metadata: provenance, attribution, permission/status for storage, display, annotation, and evaluation use.

This is a conceptual contract, not a proposed database schema. Rights statuses record what is known and permitted; they do not make legal determinations.

### Original material and stored document payload

The original source must remain separate from parser output. A stored or imported text/file payload is an artifact behind Source, not a separate narrative entity in V1. Derived normalized text, parser blocks, and indexes can be regenerated; they must not overwrite the received original.

For screenplay text, preserve the original content exactly as imported. If processing needs normalized line endings or other normalization, retain a mapping back to the original offsets. For a film Source, retain a stable reference and the metadata/provenance that can lawfully be stored; do not assume the film itself is an available payload.

## 4. Ingestion and screenplay parsing

Ingestion is deterministic where possible and reproducible from a pinned source revision. Parser output is derived information. The parser's current categories remain:

- scene_heading
- action
- character
- dialogue
- parenthetical
- transition
- blank

The existing parser's ScriptBlock is currently only a type and text pair; it strips surrounding line whitespace and does not preserve line numbers or character offsets. It classifies lines, but does not assemble Scenes or establish canonical Character identities. Those are known limitations, not capabilities this architecture assumes already work.

### Proposed deterministic processing sequence

~~~text
RAW SOURCE
  → preserve original + identify source revision
  → decode / normalize in a reversible derived view
  → classify source lines into existing block categories
  → preserve source positions for every block
  → propose scene boundaries from scene-heading blocks
  → detect and normalize character cues as candidates
  → create or update source-linked representation records
  → calculate deterministic structural properties
  → offer uncertain candidates for human review
~~~

The stages that turn a detected cue into a canonical Character, or a heading into an accepted Scene, need explicit identity and review rules. A parser candidate is not automatically a curated narrative interpretation.

### Source position and stable IDs

Every parser block and constructed Scene must retain a location in the exact Source revision. The locator design should support:

- source line numbers, including a clear one-based or zero-based convention;
- start and end character offsets with a declared character encoding/index convention;
- source spans for a block, scene, excerpt, and evidence item;
- mapping from any normalized processing view back to the original source;
- stable Scene and block IDs that survive reprocessing of unchanged content;
- source-revision qualification so anchors do not silently drift after edits.

Prefer IDs based on a stable source/revision identity and structural locator, with explicit handling for duplicate headings or repeated text. The exact ID-generation and offset convention remain implementation decisions; a display line number alone is not a sufficiently stable evidence anchor.

### Scene construction and Character detection

Scene headings can provide a deterministic initial boundary signal. The parser should preserve pre-heading text, malformed or missing headings, and uncertain boundaries instead of dropping or forcing them into a presumed structure. Scene order is source order unless a human-curated correction says otherwise.

Uppercase cues may propose character labels. Cue normalization may group punctuation variants or parenthetical extensions, but identity merging can be wrong (for example, a generic role, a crowd cue, or two aliases). Keep raw cue text and normalized candidate separate; expose uncertain merges for review. Do not infer a full character identity, objective, relationship, or knowledge state from capitalization alone.

The phrase “structured narrative objects” does not mean all ontology objects are parser outputs. Deterministic parsing can produce source-aligned blocks, scene-boundary candidates, cue candidates, and observable appearance counts. Objectives, obstacles, information changes, mechanisms, and interpretations require separate evidence and a human-curated or validated analytical process.

### ScriptBlock is not a narrative entity

ScriptBlock is parser output and must not be treated as:

- a Beat, which is a narrative change unit within a Scene;
- Evidence, which records source support for a claim;
- an AnalysisClaim, which states a proposition and its status;
- a Scene, which is a canonical Work-scoped narrative unit mapped to source material.

Block type describes screenplay formatting/position. It does not by itself describe narrative function.

## 5. Canonical narrative representation

The following are the proposed V1 canonical concepts identified in the architecture decisions. “Canonical” means shared identity across product contexts, not necessarily an existing implemented schema.

### Canonical narrative objects

| Object | Meaning and boundary |
| --- | --- |
| Work | Narrative-level container shared by Study and Make. Ownership/provenance is separate from story identity. |
| Source | A Work-linked screenplay source or film reference with provenance, payload/reference, revision, and locator context. |
| Scene | Work-scoped narrative unit, ordered within the Work and linked to the Source span it represents. Scene Study is a view over this object. |
| Beat | A small unit in which something changes within a Scene. Explicitly curated or authored in V1; never a parser block. |
| Character | Work-scoped participant. V1 does not imply cross-Work character identity. |
| Relationship | Work-scoped relationship among Character participants. A trajectory is a set of supported claims, not a single objective numeric measure. |
| Event | Something that happens in the story world, distinct from user activity or Study History. |
| Objective | Something a Character is actively pursuing. A scene/objective link or inferred objective needs evidence and clear provenance. |
| Obstacle | Something preventing an Objective from being achieved. A relation to an Objective or Scene should be explicit and supported. |
| Information | A piece of knowledge relevant to the narrative. Who knows what and when is analytical, not a fact implied by a text keyword. |
| Mechanism | Minimal V1 concept with identity, name, and description, plus explicit occurrence/claim links. Do not assume a comprehensive taxonomy. |
| Evidence | A source-linked record supporting, challenging, or contextualizing a claim. It points to a Source revision and stable location. |
| AnalysisClaim | A proposition about a target, classified as FACT, INFERENCE, or INTERPRETATION and linked to Evidence and provenance. This is the explicit claim object proposed by the architecture decisions. |

World and Location are already named contextual concepts in the narrative model. They may be linked where the curated data requires them, but they are not prerequisites for the first intelligence MVP or standalone global destinations.

### Derived analysis

Derived analysis includes parser classifications, measurable structural properties, candidate cue groupings, search indexes, similarity scores, and analytical claims proposed by a deterministic process or a model. It must carry enough method and source provenance to be reproduced or reviewed.

Do not silently promote derived output into a canonical narrative object. A proposed objective, mechanism occurrence, relationship change, or information reveal becomes a curated record only through an explicit accepted workflow.

### User-generated objects

| Object | Meaning and boundary |
| --- | --- |
| Note / Material | User-authored freeform text, optionally linked to Work, Scene, Character, Evidence, or another supported target. It preserves the author's wording and is not automatically a fact or corpus annotation. |
| Annotation | User-authored, source-span and/or Scene-anchored note or tag. It remains distinct from Evidence and AnalysisClaim even if it references them. |
| UserReference | A user's saved association to an existing Work, Scene, or Mechanism. It points to the canonical target rather than copying it. Reference Shelf is a view over these associations. |

User ownership and access control are system-level relationships rather than narrative entities. Private user material is not reused for corpus, evaluation, or training by default; any such use would require a separate, explicit governance decision.

### Source artifacts and non-entities

- A screenplay file or stored text payload is an artifact behind Source, not a narrative Document entity in V1.
- Film and Screenplay are Source kinds/representations attached to Work by default, not Work subtypes.
- Creator remains Work metadata in V1; no Creator entity is required.
- Analysis is a view/grouping of AnalysisClaims, not a separate canonical narrative entity.
- Interpretation is the status of a claim, not a separate object.
- ScriptBlock and parser classifications are derived representation records, not canonical narrative objects.
- Structural Unit, typed Narrative State, Draft, Version, Theme, Motif, Setup, Payoff, and Convention remain deferred objects as specified in the architecture decisions.

## 6. Structural analysis

The first analysis layer should be deterministic, inspectable, and useful without a large language model. It describes what is countable or linkable in a parsed representation.

Candidate V1 structural outputs include:

- scene count and source order;
- scene length, with the unit declared (for example, source lines or characters; do not infer page counts without a page-layout model);
- action/dialogue block counts and proportions;
- character cue and appearance counts;
- character co-occurrence by Scene;
- location labels and recurrence when headings or curated data provide them;
- dialogue-block counts by character cue;
- transition-block type and position;
- source-span coverage and Scene-to-Source relationships;
- basic chronology when explicit source/curatorial metadata supports it;
- explicit structural metadata supplied by a curator.

Each computed value should be traceable to its input representation and method. Re-running the same method against the same Source revision should yield the same output.

Structural summaries reveal patterns; they do not assign quality, correctness, or prescribed act structure. A Work with few conventional scene headings remains a valid Work. V1 may show ordered Scenes and contextual structure claims; it must not fabricate Acts, Sequences, or other Structural Units from sequence numbers.

Semantic analysis is a separate layer. Goals, obstacles, state changes, information asymmetry, mechanisms, and explanations are not direct consequences of a word count or block label. A semantic result must be represented as an evidence-backed AnalysisClaim, a human-curated narrative record with provenance, or an explicitly uncertain model proposal.

## 7. AnalysisClaim, Evidence, and status

### Claim structure

An AnalysisClaim is a proposition about one or more explicit targets. The target may be a Work, Scene, Character, Relationship, Event, Objective, Obstacle, Information item, or Mechanism occurrence, as supported by the V1 model. A claim should identify:

- target or targets;
- concise proposition/claim text;
- status: FACT, INFERENCE, or INTERPRETATION;
- one or more Evidence records for a claim presented as established analysis;
- provenance: how it was produced, by whom or what, and from which Source revision;
- author/source identity and review state;
- optional confidence only when the scale has a defined and evaluated meaning.

Claims with multiple sources or targets should make those links explicit. One claim may have multiple Evidence records. Evidence may support or challenge more than one claim. A hypothesis without source Evidence may remain a user Note or an unaccepted model proposal; it must not be presented as an established AnalysisClaim.

### Status definitions

| Status | Definition | Example form |
| --- | --- | --- |
| FACT | A directly observable property of the source or its explicit metadata, stated narrowly enough that a reader can verify it. | “At the cited locator, the original text reads EXT. STATION – NIGHT.” |
| INFERENCE | A conclusion derived from one or more observable source details but not literally stated by them. The derivation and supporting evidence should be inspectable. | “The two characters likely recognize the signal before the audience is told its origin.” |
| INTERPRETATION | A reasoned explanation of what an observed or inferred pattern may be doing in the work. It is contestable and should remain visibly interpretive. | “The delayed identification may shift the scene from procedural suspense toward grief.” |

Do not label an interpretation FACT because it is confidently phrased or repeated in secondary material. Confidence, if later used, measures a declared uncertainty target; it does not convert one status into another.

### Evidence requirements

Evidence must resolve to the stable Source revision and location it cites. Store or derive a short excerpt only where rights and product policy allow. Keep separate:

- the quoted/observed source material;
- a neutral observation about that material;
- the claim it supports or challenges;
- the method and author/provenance of that claim.

Evidence is not a user annotation, and a claim is not evidence. A human-written interpretation still needs source support when it makes a claim about a Work. The product can preserve a question or hypothesis as a Note without falsely presenting it as evidenced analysis.

## 8. Capability matrix: deterministic, model-assisted, human-curated

These are initial method recommendations, not current implementation claims. Model assistance always remains reviewable; a model score alone is not ground truth.

| Analytical task | Initial capability | Boundary / review |
| --- | --- | --- |
| Source decoding, line mapping, block classification | DETERMINISTIC | Preserve original source and locators; report unsupported formats or uncertain classifications. |
| Scene segmentation | DETERMINISTIC | Use explicit heading patterns as boundary signals; expose malformed/ambiguous boundaries for review. |
| Character cue normalization | DETERMINISTIC + rule-based | Keep raw cues and aliases; uncertain identity merges require review. |
| Scene count, order, length, dialogue/action distribution, transitions | DETERMINISTIC | Publish units and method; do not assign narrative quality. |
| Character appearance and co-occurrence | DETERMINISTIC from accepted cues/Scenes | Results depend on reviewed cue identity and source alignment. |
| Character objective | MODEL-ASSISTED + HUMAN-REVIEWED | Require specific evidence; preserve alternatives and disagreement. |
| Scene objective and obstacle | MODEL-ASSISTED + HUMAN-REVIEWED | Avoid forcing one objective or conflict into every Scene. |
| Information introduction, discovery, reveal, withholding, misunderstanding | MODEL-ASSISTED + HUMAN-REVIEWED | Evidence must support who knows what and when; keyword hits alone are insufficient. |
| Relationship, power, trust, dependency, or strategy change | MODEL-ASSISTED + HUMAN-CURATED | Keep Characters and Relationships Work-scoped; do not treat undefined numeric scales as facts. |
| Narrative mechanism | MODEL-ASSISTED + HUMAN-CURATED TAXONOMY INITIALLY | Start with a small descriptive vocabulary and allow variants, “other,” and uncertain cases. |
| Structural hierarchy | HUMAN-CURATED INITIALLY | Do not infer Act/Sequence hierarchy from a fixed formula or scene order. |
| Interpretive explanation | MODEL-ASSISTED, EVIDENCE-GROUNDED, HUMAN-REVIEWED FOR CORPUS | Label INTERPRETATION; allow multiple reasonable explanations. |
| Cross-Work structural similarity | RETRIEVAL / MODEL-ASSISTED + HUMAN EVALUATION | Return comparison dimensions and explanations; separate structural similarity from surface resemblance or influence. |
| Historical influence | HUMAN-CURATED / SOURCE-ATTRIBUTED RESEARCH | Similarity alone cannot establish influence. |
| Visual observations and art interpretation | FUTURE VISION-LANGUAGE ASSISTANCE + HUMAN REVIEW | Keep observation, inference, and interpretation separate and cite image regions/context. |

Do not deploy an LLM just because a feature contains the word “analysis.” Deterministic measurements, explicit curation, and a useful source viewer may solve the problem more reliably.

## 9. Narrative knowledge corpus

The corpus is a central product and research asset. It includes more than source works: it includes structured, provenance-aware understanding of those works.

### Two related corpus layers

1. **Source corpus** — identified Works and Sources with provenance, rights/access status, and preserved original material or external reference.
2. **Annotated / structured corpus** — reviewed narrative representation, structural outputs, AnalysisClaims, Evidence, curator annotations, and permitted comparison links over source works.

The second layer is what can support retrieval, evaluation, and later model development. It must remain possible to tell curated material from user-private Notes and model-generated proposals.

For a curated Work, the corpus may contain:

- Source and Work metadata;
- Scenes and source spans;
- Characters and reviewed cue/appearance links;
- Relationships and supported changes;
- Events and explicit chronology/causal relations where available;
- Information records and claims about knowledge/revelation;
- Objectives and Obstacles;
- Mechanisms and occurrence/claim links;
- AnalysisClaims and their Evidence;
- user-agnostic curator notes where appropriate and rights permit.

Not every Work needs every object type or a complete analysis. Missing data is not evidence that the narrative lacks that feature. Corpus completeness and review status should be explicit.

Public Story Atlas content and private user Works are separate access/governance domains even though they share object types. Do not ingest a user's writing into the research corpus or training data by default.

## 10. Annotation and gold dataset

A gold dataset is a carefully described, human-reviewed set of source-linked examples used to evaluate a task and, only if justified, to train or calibrate a specialized model. “Gold” means governed reference data under a documented annotation protocol; it does not mean one uncontestable interpretation.

In this section, dataset annotation means a research label or judgment made under that protocol. It is not the product's user-generated Annotation object, which is a private, source-span and/or Scene-anchored object. A dataset label may inform a curated AnalysisClaim after review, but it must not be conflated with a user's Annotation.

Possible records include:

- Scene → Objective → Evidence;
- Scene → Obstacle → Evidence;
- Scene → Change claim → Evidence;
- Scene → Information introduced/revealed/withheld → Evidence;
- Character/Relationship → change claim → Evidence;
- Scene → Mechanism occurrence claim → Evidence;
- Scene A ↔ Scene B → declared similarity dimensions → explanation → Evidence;
- Work → structural claim → Evidence.

Each task needs a written unit of annotation, allowed labels, evidence policy, provenance, and adjudication approach. Include:

- positive examples;
- negative examples where a tempting label is unsupported;
- ambiguous examples;
- disagreement cases and alternative interpretations;
- counterexamples to familiar patterns;
- works that deliberately violate a convention or expected structure;
- examples where annotators abstain because the source does not settle the question.

Preserve annotator-level labels and rationales when disagreement is meaningful. A consensus label may be useful for a specific evaluation, but it must not erase the underlying alternatives. Split evaluation data by Work (not just by scene) when the goal is generalization to unseen Works, so similar scenes from one Work do not leak across train and evaluation sets.

The dataset's purpose is to recognize patterns present in actual works and preserve variation, not to teach a screenplay textbook as a universal rulebook.

## 11. Training and adaptation strategy

These techniques solve different problems and should be evaluated separately:

| Technique | Role | What it does not solve by itself |
| --- | --- | --- |
| Prompting | Instructs a general model to follow a task protocol, use status labels, cite supplied evidence, and abstain when unsupported. | Does not guarantee correct source localization, stable behavior, or domain knowledge. |
| Retrieval | Supplies relevant Works, Scenes, claims, and source excerpts for a question or comparison. | Does not prove retrieved examples are structurally relevant or rights-cleared. |
| Tool use | Lets a model request deterministic counts, graph traversals, filters, or exact source spans from structured tools. | Does not make tool output an interpretation or resolve ambiguous narrative meaning. |
| Supervised fine-tuning | Adapts a model's outputs to a well-defined task using reviewed examples. | Does not repair a weak ontology, sparse evidence, contradictory labels, or rights problems. |
| Specialized classifiers | Handle bounded tasks such as block/cue categorization when a stable label set and sufficient evaluation data exist. | Do not replace broader interpretive reasoning or human review. |
| Embedding / representation learning | Supports candidate retrieval and neighborhood discovery over text or structured descriptions. | Similar vector neighborhoods do not establish narrative equivalence, influence, or explanation. |

Recommended sequence:

1. Build a structured, source-linked corpus.
2. Write annotation protocols and create reviewed gold examples, including counterexamples and disagreements.
3. Establish task-specific evaluation and simple baselines.
4. Test suitable existing foundation models with prompting, retrieval, and tools.
5. Categorize failure modes by task and determine whether they arise from source alignment, ontology, retrieval, prompts, or model capability.
6. Identify bounded tasks where specialization could improve measurable outcomes.
7. Fine-tune or train specialized components only when evaluation demonstrates a need and governance permits the data use.

The likely proprietary asset is the combination of structured narrative data, stable evidence links, comparative mappings, annotation protocols, and evaluation data—not merely access to a foundation model.

## 12. Future model architecture

Narrative Lab should be a composition of task-specific components, not one monolithic “Narrative Lab model.”

| Component | Future role |
| --- | --- |
| Deterministic parser | Reproducibly classify supported screenplay text, preserve locators, and propose scene/cue boundaries. |
| Embedding model | Retrieve candidate passages, scenes, or Works by semantic/structural description; results need a declared comparison purpose. |
| Text LLM | Explain, synthesize, or propose claims over retrieved structured context and evidence, with status labeling and abstention. |
| Vision-language model | Later, describe image content and propose visual relations/interpretations with region-level evidence. |
| Classifier | Perform bounded, evaluated categorization tasks such as a screenplay formatting class. |
| Reranker | Reorder retrieved candidates against an explicit query or comparison rubric. |
| Retrieval system | Find exact source passages, metadata matches, structured objects, and candidate comparative examples. |
| Graph queries / structured tools | Calculate counts and traverse explicit Work/Scene/Character/Event/Evidence links exactly. |
| Future fine-tuned task models | Improve a specific task only after a baseline and evaluation identify a clear benefit. |

Different tasks require different strengths: exact offsets need deterministic code; a closed formatting category may suit a classifier; a grounded explanation may use an LLM; cross-work candidate discovery may use embeddings plus a reranker and human judgment. Combine only what a measured task needs.

## 13. LLM role and interaction contract

An LLM is a reasoning and interpretation layer over structured information. It should not receive a screenplay and return an ungrounded generic essay as the default analysis path.

Preferred flow:

~~~text
USER QUESTION
  → retrieve relevant narrative objects
  → retrieve source evidence and provenance
  → run exact structured operations where needed
  → give the model bounded context and task instructions
  → generate a status-labeled claim or explanation
  → validate/source-link the answer
  → return claim + explanation + evidence + uncertainty
~~~

Possible future questions:

- “Why might this scene work?”
- “Show me what changes here.”
- “Trace this setup.”
- “Where else does this mechanism occur?”
- “Show scenes that are structurally similar.”
- “What happens downstream if this scene is removed?”
- “What is this draft spending its time on?”

The last questions involving setup tracing, structural comparison, downstream dependencies, or draft analysis depend on later capabilities and are not V1 promises.

The model should:

- identify whether it is reporting FACT, INFERENCE, or INTERPRETATION;
- cite the precise retrieved source spans and relevant canonical objects;
- show comparison criteria and why a candidate was retrieved;
- state when the source does not support an answer, or ask for human review;
- preserve alternative explanations when evidence permits more than one;
- avoid turning a user Note into a fact about the Work.

Preserve writer agency. A model can describe options and consequences, but must not act as an unquestionable authority or automatically rewrite a user's screenplay. User-authored edits and transformations require deliberate user action and later lineage decisions.

## 14. Comparative reasoning

Comparison is a future intelligence capability. The architecture should keep distinct dimensions instead of collapsing them into a generic similarity score:

| Comparison type | Question it answers | Important limit |
| --- | --- | --- |
| Surface similarity | Do the passages share wording, objects, settings, or other directly visible features? | Shared vocabulary does not imply shared narrative function. |
| Structural similarity | Do the passages perform a comparable role or sequence of changes in their respective works? | Similar structure can appear with different events, characters, genres, and settings. |
| Relational similarity | Do character roles, dependencies, power positions, or changing relationships correspond? | A relation mapping is an analytical proposal and needs evidence on both sides. |
| Formal similarity | Do the works use comparable arrangements of time, viewpoint, repetition, parallelism, or other formal devices? | Formal features need medium-aware representation and explicit comparison criteria. |
| Historical influence | Is there evidence that one work influenced another? | Similarity alone is not evidence of historical influence; require attributable historical/contextual sources. |

Two Scenes can be structurally similar despite different settings, Characters, historical periods, genres, and literal events. A comparison should report which dimensions match, which differ, what evidence supports the mapping, and whether the mapping is human-curated or model-proposed.

Retrieval provides candidates; it does not certify equivalence. Human evaluation should assess whether a result is useful and whether its explanation faithfully describes both Works.

## 15. Narrative mechanisms

The minimal V1 Mechanism concept follows the architecture decisions:

~~~text
Mechanism
- id
- name
- description
~~~

An occurrence or analytical claim links a Mechanism to a Scene, Work, or other relevant target and to its Evidence. Keep concept identity separate from a particular use in a Work.

Candidate initial labels may include objective, obstacle, confrontation, information reveal, information withholding, reversal, preparation, aftermath, and transition. These are descriptive analytical concepts, not mandatory beats, an exhaustive taxonomy, or rules that every screenplay must follow.

Start with a small curated vocabulary and allow variant descriptions, overlapping mechanisms, uncertainty, and no-match cases. Similar effects may be achieved by very different mechanisms. Do not expand into a large taxonomy until examples, annotation practice, and evaluation show that the distinctions are useful.

## 16. Information understanding

Information is an important narrative dimension, but it is not reducible to keyword extraction. The long-term representation may distinguish:

- introduction;
- discovery;
- revelation;
- withholding;
- misunderstanding;
- asymmetric knowledge;
- delayed disclosure.

The analytical question is:

~~~text
WHO KNOWS WHAT
WHEN
AND HOW THAT KNOWLEDGE CHANGES
~~~

Represent the underlying Information item separately from claims about its content, source, discovery, or distribution among Characters. A claim about who knew what at a point in the Work needs evidence and may remain uncertain or contested.

V1 can support curated Information links and evidence-backed claims where needed. Full knowledge-state timelines and setup/payoff tracing remain later capabilities. Do not turn the current untyped Scene state dictionaries into a validated Narrative State model.

## 17. Character and relationship understanding

Future analysis may examine Character goals, Objectives, Relationships, power, dependency, trust, conflict, strategy changes, and scene-by-scene relationship change.

For V1:

- Character and Relationship identity remains Work-scoped.
- Character Study is a view, not a second Character object.
- Objectives and Obstacles are explicit objects/links where curated; inferred objectives need claims and Evidence.
- A relationship change across Scenes is a supported claim or curated sequence, not a fabricated numeric trajectory.
- Numeric trust/power/attraction values must not be presented as objective measurements unless scale, evidence, and provenance are defined.
- Cross-Work Character identity, complete trajectories, and full relationship graphs remain later.

An analytical system should permit a Character to pursue competing goals, change strategy without changing goal, conceal a goal, or have no confidently inferable goal in a Scene.

## 18. Visual-art extension

Visual art is a future extension. A painting should not be forced into screenplay Scenes, dialogue, or Character beats.

Possible visual-intelligence pipeline:

~~~text
IMAGE
  → visual perception
  → objects / figures
  → spatial relations
  → gesture
  → gaze
  → composition
  → repetition / contrast
  → motif candidates
  → contextual references
  → interpretation
  → image-region evidence
~~~

A vision-language model may assist with bounded observations, but the system must preserve:

- **OBSERVATION:** “Two figures occupy opposite sides of the composition.”
- **INFERENCE:** “Their spatial separation may be significant.”
- **INTERPRETATION:** “The composition may use distance as a visual expression of alienation.”

These are different levels of claim. Symbolic meaning must not be asserted automatically as an observable fact. Evidence should be anchored to image regions and contextual sources where appropriate; confidence and model provenance should be explicit if shown.

Visual intelligence may share higher-level analytical ideas such as structure, relationship, attention, repetition, contrast, transformation, motif, and context. Those shared ideas do not require the same source structure or object types.

## 19. Cross-media architecture

The long-term system may study screenplays, films, paintings, photographs, novels, plays, and other cultural works through a common conceptual layer while preserving each medium's own representation.

~~~text
common abstraction ≠ identical representation
~~~

A screenplay Scene and a painting must not be forced to become the same object. Each medium can have its own source locators, observable units, and representation schema. Higher-level claims and comparison dimensions may be shared when they genuinely apply, with explicit mappings rather than implicit conversion.

Cross-media comparison should name the mapping being made (for example, attention, repetition, relationship, or transformation), preserve the media-specific evidence, and allow “not comparable” where no sound mapping exists. The visual pipeline and broader media ontology are future research, not V1 screenplay requirements.

## 20. Evaluation

Evaluation is a first-class subsystem. It tests whether a system is useful and source-faithful, not merely fluent.

Candidate evaluation dimensions:

- source localization and source-span alignment accuracy;
- parser block and scene-boundary accuracy;
- character cue normalization precision/recall and false identity merges;
- extraction accuracy for explicitly defined objects/relations;
- evidence grounding and evidence sufficiency;
- FACT / INFERENCE / INTERPRETATION classification;
- structural relation accuracy;
- mechanism recognition and useful “no match” behavior;
- comparison quality by declared similarity dimension;
- false-positive rate and abstention quality;
- ambiguity preservation and alternative-interpretation handling;
- agreement and disagreement across human annotators;
- usefulness to writers and researchers, assessed separately from factual correctness.

Maintain simple baselines for each task. Compare model-assisted methods against deterministic, metadata-only, or human-curated baselines as appropriate. Set evaluation splits and acceptance criteria before inspecting final test results; hold out complete Works when testing generalization to unseen Works.

### Example failure cases to test

- A convincing explanation cites a span that does not support it.
- A parser reports the right text but offsets point to a different source revision.
- An uppercase action line is mislabeled as a Character cue and creates a false Character.
- A Character alias merge combines two people or splits one Character without surfacing uncertainty.
- An interpretation is labeled FACT because the model states it confidently.
- A model finds a “reversal” in every Scene because the label set rewards forced categorization.
- A similarity result matches setting and vocabulary but not the declared structural relation.
- A similarity explanation describes only one of the two Scenes or omits contrary evidence.
- A model treats a plausible historical resemblance as proof of influence.
- A visual model treats a symbolic interpretation as directly observed content.
- A fluent answer ignores an ambiguity that human annotators preserved.
- A private user Note is exposed as curated corpus content or used as a training label without authorization.

A fluent explanation is not evidence of understanding. Evaluation must compare claims and source links against reviewed annotations and the actual source.

## 21. Human review and disagreement

For model-assisted corpus work, use a review loop such as:

~~~text
MODEL PROPOSAL
  → retrieve candidate evidence
  → human review
  → accept / modify / reject / mark ambiguous
  → retain reviewer rationale and provenance
  → approved gold data or evaluation case
  → future system evaluation
~~~

Keep the raw proposal, evidence, reviewer decision, and any edited claim distinguishable. Acceptance should not erase who proposed or reviewed a claim. Rejection can be valuable negative data when the reason is captured.

Experts may reasonably disagree about an interpretation. Preserve multiple claims, authors, and rationales where appropriate; do not force a single interpretation merely to simplify a schema. Adjudication can create a task-specific reference answer while retaining the disagreement record.

## 22. Provenance

Every important analytical artifact should answer:

- Where did this come from?
- Which Work, Source, and Source revision does it concern?
- Who or what created it?
- Was it directly extracted, deterministically derived, model-generated, human-curated, or user-authored?
- What source evidence supports, challenges, or contextualizes it?
- Has a human reviewed it, and what decision did they make?

For future model outputs, retain as appropriate:

- model/component identifier and version;
- prompt/task specification version;
- retrieval context and retrieved object/source IDs;
- tool calls or structured operations used;
- source evidence and source revision;
- generation time and review status.

This is an architectural principle, not a requirement to implement a provenance platform now. Provenance must not be inferred after the fact from the prose of a claim.

## 23. Rights and corpus governance

Corpus construction must track, at minimum:

- source provenance and attribution;
- copyright or usage status as known;
- permission/status to store the source;
- permission/status to display or quote it;
- permission/status to annotate and evaluate against it;
- permission/status for model training or other research use;
- any access or retention restrictions;
- whether material is internal research corpus or public user-facing content.

Do not treat permission for one purpose as permission for every purpose. Keep access decisions attached to the relevant Source and corpus use. Separate internal annotations from public-facing content when required by the governing rights and product policy.

This section defines information the architecture must preserve; it provides no legal conclusion. Rights review and source access are prerequisites for corpus work, not properties a language model can infer.

## 24. First intelligence MVP

The first intelligence research milestone should test a narrow end-to-end result on a deliberately bounded screenplay set. It should establish whether Narrative Lab can reliably produce:

1. Scene structure linked to stable source positions.
2. Character cue/appearance structure with uncertain identity cases visible.
3. Source-linked observations.
4. A small set of evidence-backed analytical claims with explicit status.
5. Useful retrieval of similar narrative situations, with a human-readable comparison rationale.

This is a research milestone, not a promise that all five capabilities ship in V1. The initial product loop remains Study / Make with shared narrative objects, inspectable structure, Evidence, and user Notes/Annotations. Deterministic parsing and human-curated analysis may be enough for a first usable experience.

Do not attempt in this MVP:

- full screenplay interpretation;
- autonomous story criticism or quality scoring;
- comprehensive thematic analysis;
- a complete or prescriptive narrative ontology;
- all-media intelligence;
- autonomous screenplay rewriting;
- a full knowledge graph or all-work comparison engine.

## 25. Research experiment plan

Run these as staged experiments. For each task, define the annotation unit, baseline, dataset split, and acceptance threshold before evaluating held-out results. The success criteria below define a pass condition without inventing numeric thresholds before a corpus and annotation protocol exist.

### Experiment 1 — Screenplay parsing and source alignment

- **Question:** Can supported screenplay text be classified and navigated while preserving exact source alignment?
- **Input:** A rights-cleared set of screenplay text files or pasted text with varied formatting, including malformed or missing headings.
- **Expected output:** Original source identity; classified blocks in the existing categories; line/character locators mapped to original text; scene-boundary candidates and uncertainty flags.
- **Evaluation:** Compare block types and scene boundaries with human labels; test that every emitted span resolves to the exact intended original substring after processing and reprocessing.
- **Success criterion:** Source spans round-trip to the pinned original revision, errors are measurable and categorized, and the boundary/formatting limitations are understood well enough to set a justified V1-supported input scope.
- **What it unlocks next:** Evidence anchoring, stable Scene construction, and character-cue evaluation.

### Experiment 2 — Scene, Character, and Event representation

- **Question:** Can parsed sources be represented with stable Scenes and useful, reviewable Character/Event links without hiding uncertainty?
- **Input:** Experiment 1 outputs plus a small human-annotated set of scenes, cue aliases, appearances, and explicit story-world Events.
- **Expected output:** Stable Work-scoped Scene records, Character cue candidates and reviewed identity links, source spans, and explicitly supported Event relations.
- **Evaluation:** Measure scene boundary accuracy, cue normalization precision/recall, false alias merges, and agreement for event links; inspect errors by formatting and work.
- **Success criterion:** Scene and cue errors are visible and reproducible; accepted IDs remain stable for unchanged source; canonical links are not silently created from uncertain cues.
- **What it unlocks next:** Source-grounded observation and claim extraction.

### Experiment 3 — Evidence-backed claim extraction

- **Question:** Can a system propose narrow claims and attach evidence that actually supports them?
- **Input:** Reviewed representation and a task-bounded set of observable claims with human-labeled status and source spans.
- **Expected output:** Candidate AnalysisClaims with target, FACT/INFERENCE/INTERPRETATION status, cited Evidence, provenance, and abstention when unsupported.
- **Evaluation:** Score claim correctness, status classification, source-span sufficiency, unsupported claims, and abstention against held-out Works and human review.
- **Success criterion:** Reviewers can verify each accepted claim from its cited source, unsupported claims are measurable, and status errors are not obscured by fluent prose.
- **What it unlocks next:** Human-reviewed semantic annotation and corpus claim workflows.

### Experiment 4 — Human-reviewed Objective, Obstacle, and Information annotations

- **Question:** Can annotators consistently create evidence-linked labels for goals, obstacles, and information changes while preserving ambiguity?
- **Input:** A bounded Scene set, an annotation protocol, source spans, and independent annotators.
- **Expected output:** Human-reviewed dataset labels and/or curated Objective/Obstacle/Information claims, evidence links, alternatives, abstentions, and disagreement records. These dataset labels are not user-generated Annotation objects.
- **Evaluation:** Measure agreement by label and evidence quality; audit disagreements and cases where no single answer is justified.
- **Success criterion:** The protocol yields reproducible labels where the source supports them and preserves alternatives/uncertainty where annotators reasonably differ; disagreement is not forced into false consensus.
- **What it unlocks next:** A governed gold set for semantic assistance and information-flow experiments.

### Experiment 5 — Mechanism recognition

- **Question:** Does a small curated mechanism vocabulary help identify useful narrative operations without forcing every Scene into a category?
- **Input:** Human-reviewed mechanism occurrences, non-occurrences, ambiguous cases, and counterexamples across varied Works.
- **Expected output:** Candidate Mechanism links or claims with Evidence, alternative labels, and a valid no-match/abstain result.
- **Evaluation:** Compare deterministic/text retrieval and model-assisted proposals against human-reviewed labels; measure false positives and utility of explanations.
- **Success criterion:** The method retrieves supported examples better than a simple baseline under predeclared criteria while preserving no-match and variant cases; label pressure does not create a mechanism in every Scene.
- **What it unlocks next:** Mechanism retrieval and controlled comparison across Works.

### Experiment 6 — Structural similarity retrieval

- **Question:** Can retrieval find Scenes that perform comparable structural work even when their surface details differ?
- **Input:** Human-curated Scene pairs labeled by surface, structural, relational, and formal similarity separately, including difficult negative pairs.
- **Expected output:** Ranked candidate pairs, dimension-specific similarity reasons, source Evidence on both sides, and explicit differences.
- **Evaluation:** Human rate relevance and explanation faithfulness; compare against metadata-only and surface-text baselines; audit false matches and held-out Works.
- **Success criterion:** Results provide useful, evidence-supported structural matches beyond surface/metadata baselines under predeclared criteria, and the system does not describe similarity as historical influence.
- **What it unlocks next:** A comparison workspace research prototype and query patterns for retrieval.

### Experiment 7 — LLM reasoning over structured narrative data

- **Question:** Does an LLM add useful reasoning when restricted to retrieved objects, evidence, and deterministic tools?
- **Input:** User-like research questions, structured Work/Scene data, source Evidence, tool outputs, and examples requiring abstention or multiple interpretations.
- **Expected output:** Status-labeled explanations with source citations, relevant object links, uncertainty/alternatives, and no unsupported factual assertions.
- **Evaluation:** Compare grounded responses with a direct-screenplay prompt and a no-LLM retrieval baseline; assess evidence faithfulness, status correctness, abstention, and usefulness with researchers/writers.
- **Success criterion:** The structured flow improves usefulness on the chosen task without reducing source faithfulness or ambiguity preservation; fluent unsupported responses fail.
- **What it unlocks next:** A bounded reasoning layer for selected Study questions, not a general screenplay critic.

### Experiment 8 — Visual-art representation

- **Question:** Can a visual system separate observable composition from inferred relation and interpretation while citing image regions?
- **Input:** A rights-cleared, intentionally small image set with human annotations for objects/figures, spatial relations, gesture/gaze, composition, contextual references, and alternative interpretations.
- **Expected output:** Region-grounded observations, separately labeled inferences and interpretations, provenance, and disagreements.
- **Evaluation:** Review region localization, observation accuracy, interpretation overreach, ambiguity preservation, and agreement among qualified reviewers.
- **Success criterion:** Observations can be checked against image regions; speculative meaning is visibly labeled and not presented as directly observed; the result demonstrates a useful medium-specific representation without coercing it into screenplay Scenes.
- **What it unlocks next:** A separate visual-art research track and carefully chosen cross-media abstractions.

## 26. Final architecture diagram

~~~mermaid
flowchart TD
    S["SOURCE CORPUS<br/>Work · Source · provenance · rights"]
    I["INGESTION / PARSER<br/>preserve original · classify · locate"]
    C["CANONICAL NARRATIVE MODEL<br/>Work · Scene · Character · links"]
    A["STRUCTURAL + SEMANTIC ANALYSIS<br/>deterministic measures · reviewed claims"]
    E["EVIDENCE + ANALYSIS CLAIMS<br/>stable source spans · status · provenance"]
    G["ANNOTATED / EVALUATED CORPUS<br/>curated labels · disagreements · gold data"]
    R["RETRIEVAL + COMPARISON<br/>candidates · explicit dimensions · rationale"]
    M["LLM / VLM / SPECIALIZED MODELS<br/>task-specific · grounded · reviewable"]
    U["STUDY + ATLAS + WRITING STUDIO<br/>contextual views over shared objects"]
    N["USER NOTES / ANNOTATIONS / TRANSFORMATIONS<br/>private authorship · explicit links"]

    S --> I --> C --> A --> E --> G --> R --> M --> U --> N
    N -. "user-authorized links; not corpus facts by default" .-> C

    H["HUMAN REVIEW"]
    D["GOLD DATA"]
    V["EVALUATION"]
    Q["MODEL / METHOD IMPROVEMENT"]
    H --> D --> V --> Q --> H
    E --> H
    M --> H
    V -. "measured changes only" .-> A
~~~

The feedback loop improves methods and reviewed data; it does not turn every model proposal into truth. Human review, source evidence, and rights governance remain necessary as the system grows.
