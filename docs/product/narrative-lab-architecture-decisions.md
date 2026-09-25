# Narrative Lab Architecture Decisions

## Purpose and audit basis

This is a cross-document audit of:

- `docs/architecture/narrative-model.md`
- `docs/design/studio-derived-system.md`
- `docs/design/studio-feature-inventory.md`
- `docs/product/narrative-lab-feature-map.md`
- `docs/product/narrative-lab-screen-map.md`

It identifies where product/screen concepts do not yet have a consistent narrative-model meaning. This document proposes V1 resolutions, but does **not** alter the existing ontology or application code. The canonical-model section is a proposal to review before implementation.

### Resolution labels

- **MUST DECIDE NOW** means the object distinction or relationship must be agreed before a dependent V1 workflow or data contract is implemented.
- **CAN DEFER** means V1 can omit the entity or use a narrower view without closing the later design space.
- A resolution marked **proposed** is a recommendation for the product source of truth, not an already implemented or user-approved schema change.

## Cross-document classification summary

| Concept | Current classification / representation | Proposed V1 classification |
| --- | --- | --- |
| Work | Existing narrative entity; Pydantic model. | Canonical narrative entity; same identity in Study and Make, with ownership/provenance kept separate from story content. |
| Film | Mentioned as a medium/work example; no Film model. | Source/representation kind attached to a Work, not a separate entity by default. |
| Screenplay | Work example and screenplay text in feature/screen maps; parser returns ScriptBlocks only. | A Source representation of a Work; not a second Work solely because it is screenplay text. |
| Source | `Work.source` string; `Evidence.source_id` string; product docs require source spans. | New V1 entity with stable identity and provenance. |
| Document | Used as a generic source/document term in product docs; no model. | Stored/imported artifact behind a Source, not a separate narrative entity in V1. |
| Creator | `Work.creator: list[str]`; Atlas/search metadata. | Work metadata strings in V1; canonical Creator entity deferred. |
| Character | Existing narrative concept and Pydantic entity with `work_id`. | Existing Work-scoped entity. Character Study is a contextual view. |
| Scene | Existing narrative concept and Pydantic entity with sequence/links. | Existing Work-scoped entity; source span relationship must be added/defined. |
| Beat | Existing concept and Pydantic entity with `scene_id`/`order`. | Existing entity; V1 entries are explicit/curated/user-authored, not inferred by the parser. |
| Event | Existing concept and Pydantic entity. | Existing Work-scoped entity linked to scenes, participants, time, and causal relations. |
| Structural Unit | Concept in narrative-model document; absent from Pydantic schemas. | Deferred entity; V1 uses ordered scenes and a structural view. |
| Narrative State | Concept in narrative-model document; Scene has untyped `state_before`/`state_after` dictionaries. | V1 derived/curated state-change claims; typed state entity deferred. |
| Relationship | Existing concept and Pydantic entity with participant IDs and measures. | Existing Work-scoped entity; trajectory is later. |
| Objective / Obstacle | Existing concepts and Pydantic entities. | Existing entities; explicit links from scenes and characters required for V1 anatomy. |
| Information | Existing concept and Pydantic entity. | Existing entity; V1 contextual view, full information flow later. |
| Mechanism | Concept in narrative-model document; absent from Pydantic schemas; used as a V1 Work/Reference object. | Minimal V1 canonical concept entity; cross-work taxonomy/tracing later. |
| Note | Notebook/material feature in product docs; no narrative-model/schema object. | New user-generated freeform object, optionally linked to narrative objects. |
| Annotation | Basic source/scene-anchored annotations in product docs; no model; Studio Script Lab is placeholder-only. | New user-generated anchored object, distinct from Note and Evidence. |
| Evidence | Existing narrative concept and Pydantic entity, but its source/claim relationships are weakly typed. | Existing entity, linked to Source and to an explicit AnalysisClaim. |
| Analysis | Product screens/features show analysis as panels/sections; no Analysis object. | Derived view/grouping of claims, not a canonical narrative entity. |
| Interpretation | Core principle in narrative-model document; no claim-status field in schema. | A claim classification, not a separate entity. |
| Reference | Saved-work/scene/mechanism behavior in feature map; no model. | New user-to-object reference record/link, not a duplicate Work/Scene. |
| Reference Shelf | Product/screen-map destination; no narrative ontology object. | Contextual collection view over Reference records, not an entity. |
| Study History | Later feature in product map; static examples in Studio inventory. | Later user activity/StudyRecord concept, distinct from narrative Event. |
| User Work | Make-mode Work in product map; no user/ownership model. | Existing Work entity plus user ownership/provenance; not a Work subtype. |
| Draft | Later Make feature; no model. | Future user-generated source/work state, not V1. |
| Version | `Work.version: Optional[str]`; no version history model. | Future immutable revision/source snapshot entity; current string is metadata only. |
| Theme / Motif / Setup / Payoff / Convention | Concepts in narrative-model document; several are later product features; no Pydantic schemas. | Future entities, except no V1 requirement for their standalone views. |

## Decision records

### Work

- **CONCEPT:** Work.
- **WHERE IT APPEARS:** `narrative-model.md` §Work; `backend/app/schemas/narrative.py` `Work`; feature map V1-03/V1-10; screen map V1-03/V1-10.
- **CURRENT REPRESENTATION:** Existing entity with title, creator strings, year, medium, language, genre, source string, and version string.
- **PROBLEM:** The conceptual document uses Work for both a complete narrative and examples such as screenplay/film; the product map also uses Work as the user's editable object. Ownership, source identity, and narrative identity are not separated.
- **V1 REQUIREMENT:** A canonical Work identity shared by Study and Make, with linked source material and object records.
- **PROPOSED RESOLUTION:** Keep Work as the narrative-level container. Add ownership/provenance as a separate system relationship; do not create a separate `UserWork` subtype. Treat source material as linked Source records.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — confirm the Work/source boundary and ownership relationship before persistence or import behavior is implemented.

### Film

- **CONCEPT:** Film.
- **WHERE IT APPEARS:** Narrative-model Work examples; product principle “FILM / SCREENPLAY”; feature map Work Page/Story Atlas; screen map Work Page.
- **CURRENT REPRESENTATION:** No Film entity. `Work.medium` is a string; `Work.source` is an optional string.
- **PROBLEM:** The documents alternate between film as the work, film as a medium, and film as source material. Film and screenplay content may differ.
- **V1 REQUIREMENT:** Users can study a film's narrative and access the screenplay/source used for textual analysis when available.
- **PROPOSED RESOLUTION:** Film is a Source kind/representation attached to a Work, not a separate entity by default. A distinct adaptation may be a separate Work only when editorially treated as a distinct narrative work; do not infer this from file type.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — establish this default before curating multi-source Works; defer detailed adaptation-link types until needed.

### Screenplay

- **CONCEPT:** Screenplay.
- **WHERE IT APPEARS:** Product principle and V1 loop; feature map V1-04/V1-10/V1-11; screen map Scene Study/Writing Studio; `backend/app/parsers/screenplay.py`.
- **CURRENT REPRESENTATION:** The parser returns `ScriptBlock(type, text)` records. It strips each line and does not retain line numbers or source offsets. No Screenplay or Source model exists.
- **PROBLEM:** Screenplay is sometimes presented as a Work and sometimes as text within a Work. Scene and evidence views require stable source locations.
- **V1 REQUIREMENT:** Display original screenplay text, navigate scenes, and anchor evidence/annotations without losing the source.
- **PROPOSED RESOLUTION:** Treat screenplay text as a Source representation owned by a Work. Preserve original text separately from parser output. ScriptBlocks are derived parser output, not canonical narrative entities.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — source identity, immutable-original behavior, and V1 import format. Rich screenplay editing can defer.

### Source

- **CONCEPT:** Source.
- **WHERE IT APPEARS:** `Work.source`; `Evidence.source_id`; narrative-model Evidence; feature map source intake/evidence; screen map source spans and source-preserving parser.
- **CURRENT REPRESENTATION:** Optional free-text field on Work and an unvalidated string ID on Evidence; no Source entity.
- **PROBLEM:** Source text, film reference, parser result, source location, and screenplay version cannot be reliably distinguished or linked.
- **V1 REQUIREMENT:** Evidence and annotations must locate original source material; Works may have a film reference and screenplay text.
- **PROPOSED RESOLUTION:** Add a canonical V1 `Source` entity belonging to a Work, with a source kind/medium and a stable pointer to original material. Scenes, Evidence, and Annotations reference Source identity plus stable spans/locations. Do not treat parser output as source.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — entity identity, ownership relation, supported source kinds, and stable location strategy.

### Document

- **CONCEPT:** Document / source artifact.
- **WHERE IT APPEARS:** Feature map and screen map use “source/document” for screenplay intake and text display; no current schema.
- **CURRENT REPRESENTATION:** No entity or artifact model.
- **PROBLEM:** “Document” could mean a screenplay's narrative source, an uploaded file, stored text, or a format-specific file wrapper.
- **V1 REQUIREMENT:** Preserve/import screenplay material and retain enough location data for evidence.
- **PROPOSED RESOLUTION:** Do not add a separate narrative `Document` entity in V1. A Source is the domain record; its imported/stored file or text payload is an implementation artifact referenced by Source. Add a separate artifact/version concept only if multiple files/encodings need independent identity.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — decide what is stored and how a Source resolves to its payload. A separate Document entity can defer.

### Creator

- **CONCEPT:** Creator.
- **WHERE IT APPEARS:** Narrative-model Work.creator; Pydantic `Work.creator: list[str]`; feature map Story Atlas/Search; screen map metadata rows.
- **CURRENT REPRESENTATION:** List of strings on Work; no Creator schema.
- **PROBLEM:** Feature text sometimes capitalizes Creator as a narrative object, which implies a canonical entity and cross-work identity that the model does not provide.
- **V1 REQUIREMENT:** Display and search credited creator names as Work metadata.
- **PROPOSED RESOLUTION:** **Creator is simple Work metadata in V1.** Keep names/credits on Work; do not create Creator profiles or relationships. Add a Creator entity later only if authority control, role-specific credits, or creator pages become necessary.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — use metadata-only in V1. Canonical creator identity can defer.

### User and User Work

- **CONCEPT:** User / User Work.
- **WHERE IT APPEARS:** Feature map Make/My Works/Notebook/Reference Shelf; screen map My Works, ownership, permissions; no User model in narrative docs/schemas.
- **CURRENT REPRESENTATION:** No user, owner, or permission representation. Work has no owner field.
- **PROBLEM:** “User Work” may be mistaken for a new narrative entity; private notes/references cannot be scoped without ownership.
- **V1 REQUIREMENT:** Keep a user's Work, Notebook, annotations, and saved references private and connected to the right owner.
- **PROPOSED RESOLUTION:** A User Work is a normal Work plus a user-ownership relationship and provenance. User identity/permissions are system-domain concepts, not narrative objects. Do not fork Work fields by mode.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — decide whether V1 has accounts, local-only ownership, or another private-work model before persistence. User identity belongs in that decision.

### Character

- **CONCEPT:** Character.
- **WHERE IT APPEARS:** Narrative-model §Character; Pydantic `Character`; feature map V1-03/V1-05; screen map Work/Scene/Character Study.
- **CURRENT REPRESENTATION:** Existing entity with `work_id`, descriptive fields, desires, objectives, beliefs, fears, values, secrets, capabilities, limitations, and commitments.
- **PROBLEM:** The concept is broadly aligned, but narrative identity is currently Work-scoped and the product could imply cross-Work character identity or trajectory analysis.
- **V1 REQUIREMENT:** Explore a character inside one Work, follow their scene appearances, and open related evidence/relationships.
- **PROPOSED RESOLUTION:** Keep Character as a Work-scoped entity in V1. Character Study is a contextual view, not a separate entity. Cross-work identity/trajectory is not implied.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — preserve Work scope in V1. Cross-work character identity can defer.

### Scene

- **CONCEPT:** Scene.
- **WHERE IT APPEARS:** Narrative-model §Scene; Pydantic `Scene`; feature map V1-03/V1-04/V1-06; screen map Scene Study and workspace.
- **CURRENT REPRESENTATION:** Existing entity with Work ID, sequence, optional location/time, character/objective/obstacle/information/event/beat ID lists, source text fields, state dictionaries, and narrative functions.
- **PROBLEM:** The parser does not construct Scene records, and the model does not identify which Source span a Scene covers. Product screens assume stable scene navigation.
- **V1 REQUIREMENT:** A scene must be ordered within a Work and point to the screenplay/source segment it represents.
- **PROPOSED RESOLUTION:** Keep Scene as a canonical Work-scoped entity; add an explicit Source-span relation in the future schema. Treat Scene Study as a contextual workspace over that entity.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define scene-to-source mapping and stable identity. Advanced cross-scene graph links can defer.

### Beat

- **CONCEPT:** Beat.
- **WHERE IT APPEARS:** Narrative-model §Beat; Pydantic `Beat`; feature map Scene Study/Screenplay Lab; screen map screenplay annotations.
- **CURRENT REPRESENTATION:** Existing entity with `scene_id`, `order`, trigger/action/response/change, and evidence IDs. The screenplay parser does not extract beats.
- **PROBLEM:** Product language may conflate a narrative Beat with a parser block or a user annotation.
- **V1 REQUIREMENT:** If shown, a Beat is a narrative change unit linked to a Scene and supported by evidence; it is not equivalent to screenplay formatting blocks.
- **PROPOSED RESOLUTION:** Keep Beat as an existing narrative entity. V1 Beats are explicitly curated or user-created; parser classifications remain derived ScriptBlocks. Do not require automatic beat extraction.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define this distinction before tagging/annotation behavior. Automated beat inference can defer.

### Event

- **CONCEPT:** Narrative Event.
- **WHERE IT APPEARS:** Narrative-model §Event; Pydantic `Event`; Scene `event_ids`; product anatomy/work relationships.
- **CURRENT REPRESENTATION:** Existing Work-scoped entity with participants, location, narrative time, chronological position, causal predecessors/consequences, and visibility.
- **PROBLEM:** Product navigation also uses “recent events/history,” which could be confused with narrative Events. Event relations to Scenes are only ID lists.
- **V1 REQUIREMENT:** Represent story-world events only when needed to explain a Work/Scene analysis.
- **PROPOSED RESOLUTION:** Keep Event as a narrative entity. Reserve a different name such as StudyActivity for later user activity/history; never store app usage as a narrative Event.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — distinguish narrative Event from product activity. Rich causal graph can defer.

### Structural Unit

- **CONCEPT:** Structural Unit.
- **WHERE IT APPEARS:** Narrative-model §Structural Unit; feature map Work Page/Narrative Anatomy; screen map Scene Index and anatomy.
- **CURRENT REPRESENTATION:** Conceptual entity with parent/children/order/function in the architecture document; no Pydantic schema. `Scene.sequence` exists.
- **PROBLEM:** V1 needs ordered scenes and a structure view, but a fully nested Act/Movement/Sequence/Scene/Beat ontology would expand scope and has no consistent data source.
- **V1 REQUIREMENT:** Navigate an ordered scene index and display supplied/curated structure without inventing act boundaries.
- **PROPOSED RESOLUTION:** **Defer Structural Unit as a canonical V1 entity.** V1 uses `Scene.sequence` plus a contextual structure view and evidence-backed structural claims. Add typed hierarchy later if real corpus/workflows require nesting.
- **MUST DECIDE NOW / CAN DEFER:** **CAN DEFER** the entity. **MUST DECIDE NOW** that V1 will not fabricate structural units from sequence alone.

### Narrative State

- **CONCEPT:** Narrative State.
- **WHERE IT APPEARS:** Narrative-model §Narrative State; `Scene.state_before`/`state_after`; feature map Character/Relationship trajectories; screen map anatomy.
- **CURRENT REPRESENTATION:** Conceptual state components in the model document; untyped dictionaries on Scene; no Pydantic type.
- **PROBLEM:** A dictionary can mix direct source facts, user notes, and interpretation, while the roadmap expects state trajectories.
- **V1 REQUIREMENT:** Show a supported “change” claim in a Scene without presenting a complete typed state machine.
- **PROPOSED RESOLUTION:** V1 treats before/after/change as typed, evidence-linked analysis claims on a Scene/Character/Relationship. Do not create standalone NarrativeState snapshots in V1. Consider typed snapshots for later trajectories.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — do not treat current dictionaries as validated ontology. Full state model can defer.

### Relationship

- **CONCEPT:** Relationship.
- **WHERE IT APPEARS:** Narrative-model §Relationship; Pydantic `Relationship`; feature map Work Page/Character Study; screen map contextual Relationship view.
- **CURRENT REPRESENTATION:** Existing Work-scoped entity with participant string IDs, type/history, and optional bounded numeric measures.
- **PROBLEM:** Trajectory and knowledge changes are later, but product screens need basic relationship context. Numeric scales have no defined source or semantics.
- **V1 REQUIREMENT:** Navigate from Character/Scene to the relationship and its relevant scenes/evidence.
- **PROPOSED RESOLUTION:** Keep Relationship as an existing Work-scoped entity with explicit Character participants. V1 uses descriptive history and supported claims; do not present numeric dimensions as objective measurement until their meaning/provenance is defined.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define participant/link scope and treat measures as optional interpretation. Full trajectory can defer.

### Objective and Obstacle

- **CONCEPT:** Objective / Obstacle.
- **WHERE IT APPEARS:** Narrative-model §§Objective/Obstacle; Pydantic `Objective`/`Obstacle`; Scene IDs; feature map Scene Study/Narrative Anatomy.
- **CURRENT REPRESENTATION:** Existing entities; Objective has a Character ID and scope; Obstacle references Objective.
- **PROBLEM:** The product needs them in a scene view, but objective/obstacle readings can be interpretations and are not always explicit in source.
- **V1 REQUIREMENT:** Show optional objective/obstacle analysis with evidence/status; allow unavailable/uncertain states.
- **PROPOSED RESOLUTION:** Keep the entities; link Scene to Objective/Obstacle explicitly and represent the claim about them as AnalysisClaim with a type/evidence relation. Do not make parser output infer them.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — establish evidence and claim-status semantics; richer scope hierarchy can defer.

### Information

- **CONCEPT:** Information.
- **WHERE IT APPEARS:** Narrative-model §Information; Pydantic `Information`; Scene `information_ids`; feature map and screen map context views.
- **CURRENT REPRESENTATION:** Existing Work-scoped entity with content/source/timing strings and known-by/hidden-from/misunderstood-by string lists.
- **PROBLEM:** V1 uses information context, while full information-flow tracing is later; temporal strings and participant IDs are weakly typed.
- **V1 REQUIREMENT:** Link an information item to relevant scene/source and show any supplied characters/knowledge context.
- **PROPOSED RESOLUTION:** Keep Information as an existing entity; V1 provides a contextual detail/list only. Do not claim complete knowledge-state tracking. Add typed temporal/knowledge links with later information-flow work.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define minimum V1 link/provenance behavior. Full information flow can defer.

### Mechanism

- **CONCEPT:** Narrative Mechanism.
- **WHERE IT APPEARS:** Narrative-model §Narrative Mechanism; feature map Work Page/V1 Reference Shelf and later Library/tracing; screen map contextual Mechanism view.
- **CURRENT REPRESENTATION:** Conceptual entity with name, description, function, variants, and examples; no Pydantic schema or current Studio implementation.
- **PROBLEM:** V1 Work Page and Reference Shelf depend on mechanisms, while the curated Mechanism Library/tracing is explicitly later. It is unclear whether a mechanism is a reusable concept, a scene occurrence, or an analytical claim.
- **V1 REQUIREMENT:** Name a mechanism in context and link it to the Work/Scene and evidence; allow saving that concept as a reference.
- **PROPOSED RESOLUTION:** Add a minimal canonical Mechanism concept entity in V1; keep an occurrence/claim link separate and evidence-backed. Defer broad taxonomy, cross-work tracing, and full library.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — agree the concept-versus-occurrence distinction and minimal controlled vocabulary. Library/tracing can defer.

### Note

- **CONCEPT:** Note / Material.
- **WHERE IT APPEARS:** Feature map V1-13 Writer's Notebook and notes; screen map Notebook and Make flow; design-system Notebook translation. No narrative-model/schema entity exists.
- **CURRENT REPRESENTATION:** Product feature only. Studio Journal has a local draft composer but Save does not persist.
- **PROBLEM:** “Note,” “Material,” and “Notebook entry” could be one object or separate concepts; privacy and object links are unspecified.
- **V1 REQUIREMENT:** Persist private freeform text and optionally link it to Work, Scene, Character, or Evidence without converting it into a narrative fact.
- **PROPOSED RESOLUTION:** Add a user-generated Note/Material entity for freeform entries. It has an author/owner and optional links; the Notebook is a view over these notes. Keep it separate from source text and AnalysisClaim.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define privacy/ownership and the Note object boundary before persistence. Tags and media attachments can defer.

### Annotation

- **CONCEPT:** Annotation.
- **WHERE IT APPEARS:** Feature map V1-12; screen map Scene Work and annotation editor; Studio inventory identifies Script Lab's annotation copy as specification-only.
- **CURRENT REPRESENTATION:** No model/schema; no working Studio annotation workflow. Existing `Evidence` cannot safely stand in for personal annotation.
- **PROBLEM:** An annotation is anchored to source/scene context, while a Notebook Note may be freeform. Combining them without a rule makes source anchors and user authorship unclear.
- **V1 REQUIREMENT:** Add/edit/save a basic private observation or tag anchored to a Scene or stable Source span.
- **PROPOSED RESOLUTION:** Keep Note and Annotation as **separate concepts**. Annotation requires an anchor to Scene and/or Source span; it may contain a user-authored Note text and optionally link to Evidence, but it is neither Evidence nor an AnalysisClaim by itself.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — decide anchor semantics and whether Annotation owns text or references a Note. Rich annotation types/layers can defer.

### Evidence

- **CONCEPT:** Evidence.
- **WHERE IT APPEARS:** Narrative-model §Evidence/core principle; Pydantic `Evidence`; feature map V1-07; screen map Evidence view.
- **CURRENT REPRESENTATION:** Existing entity with `source_id`, claim/observation strings, optional page/line/text span/confidence. No typed target object, claim type, or guaranteed source relation.
- **PROBLEM:** Product UI needs an exact Source span, a linked claim, and FACT/INFERENCE/INTERPRETATION status. Existing `source_id` is not a validated Source relation and the claim is embedded as text.
- **V1 REQUIREMENT:** Open evidence from a claim, highlight the source, and return to the same claim/context.
- **PROPOSED RESOLUTION:** Keep Evidence as a source-support entity linked to Source and to one or more AnalysisClaims. Evidence describes what source material supports a claim; it is not the analysis itself.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — source locator and claim relation before evidence UI/data authoring. Confidence scale can defer unless used in V1.

### Analysis

- **CONCEPT:** Analysis.
- **WHERE IT APPEARS:** Feature map Work/Scene/Character/Narrative Anatomy; screen map inspector, Work Page, and Character Study; architecture document evidence principle.
- **CURRENT REPRESENTATION:** No Analysis schema/entity. Analysis is represented as screen sections and free-text model fields such as scene conflict/function.
- **PROBLEM:** A contextual view, a derived summary, and an authored claim are being called “analysis” interchangeably.
- **V1 REQUIREMENT:** Present analytical material as inspectable claims linked to a target narrative object and supporting Evidence.
- **PROPOSED RESOLUTION:** **Analysis is a derived view/grouping, not a canonical entity.** Add a proposed `AnalysisClaim` record as the authored/curated unit; a Work/Scene/Character view groups claims by target and context.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — decide whether to model AnalysisClaim separately from Evidence before V1 analysis is authored. Aggregated Analysis documents/reports can defer.

### Interpretation

- **CONCEPT:** Interpretation.
- **WHERE IT APPEARS:** Narrative-model Core Principle; feature map V1-07; screen map FACT/INFERENCE/INTERPRETATION Evidence presentation.
- **CURRENT REPRESENTATION:** Explicit conceptual distinction in docs, but no field/enum in current Pydantic models.
- **PROBLEM:** Without a typed status, the interface cannot reliably distinguish source fact from inference or interpretation.
- **V1 REQUIREMENT:** Display each AnalysisClaim's epistemic status and its supporting source Evidence.
- **PROPOSED RESOLUTION:** Interpretation is a claim classification on AnalysisClaim, not a separate entity. Use the three defined values FACT, INFERENCE, and INTERPRETATION; do not infer the value from UI section name.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define and require claim status for V1 analytical claims. More nuanced confidence/uncertainty vocabularies can defer.

### Reference

- **CONCEPT:** User Reference / saved object.
- **WHERE IT APPEARS:** Feature map V1-09 Reference Shelf; screen map Library; studio-derived documents note Studio lacks save behavior.
- **CURRENT REPRESENTATION:** No narrative entity or relationship. Atlas and library lists in Studio are static.
- **PROBLEM:** Saving a Work/Scene/Mechanism could duplicate the object rather than record a user's association to it.
- **V1 REQUIREMENT:** Save/remove/open a Work, Scene, or Mechanism from a user's Reference Shelf.
- **PROPOSED RESOLUTION:** Add a user-to-target `UserReference` record/association with stable target identity; the target stays canonical and is not copied. No sharing is implied.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — define ownership and supported targets before implementing save. Folders/annotations on references can defer.

### Reference Shelf

- **CONCEPT:** Reference Shelf / Library.
- **WHERE IT APPEARS:** Feature map navigation and V1-09; screen map top-level Library and full screen.
- **CURRENT REPRESENTATION:** Contextual screen/view; no domain object in narrative model.
- **PROBLEM:** It is unclear whether Library is the curated public Story Atlas or the user's saved objects.
- **V1 REQUIREMENT:** Distinguish catalog browsing from personal saved references.
- **PROPOSED RESOLUTION:** **Keep Library as a top-level V1 destination for the personal Reference Shelf.** Story Atlas remains inside Study. The Shelf is a view over UserReference records, not a canonical narrative entity.
- **MUST DECIDE NOW / CAN DEFER:** **MUST DECIDE NOW** — this audit resolves the current map in favor of top-level Library. Reconsider only through an explicit product-map revision, not during UI implementation.

### Study History

- **CONCEPT:** Study History / recent activity.
- **WHERE IT APPEARS:** Feature map Home and later Work/Study History; screen map Home ambiguity; Studio inventory Profile/history examples are static.
- **CURRENT REPRESENTATION:** No model. Work.version is unrelated; current screen stack is navigation state.
- **PROBLEM:** “Recent work,” current Work, saved Reference, and past Study activity are conflated.
- **V1 REQUIREMENT:** Home may show a current Work only if there is a real stored current pointer. Full activity history is not needed for the central V1 loop.
- **PROPOSED RESOLUTION:** Keep Study History out of V1. Later introduce a separate StudyActivity/StudyRecord system object; do not reuse narrative Event or UserReference.
- **MUST DECIDE NOW / CAN DEFER:** **CAN DEFER** the history entity. **MUST DECIDE NOW** that Home will not fabricate recent activity and that current-work context is not a history record.

### Draft

- **CONCEPT:** Draft.
- **WHERE IT APPEARS:** Feature map MAKE hierarchy and later Draft/Revision; screen map Writing Studio and editing-depth ambiguity.
- **CURRENT REPRESENTATION:** No Draft entity; `Work.version` is optional string metadata.
- **PROBLEM:** The feature map calls Writing Studio a user's working screenplay environment, but does not decide whether the screenplay source is editable in V1.
- **V1 REQUIREMENT:** Preserve a user's source and save V1 Notes/Annotations; do not silently imply version management.
- **PROPOSED RESOLUTION:** Defer canonical Draft entity. Proposed V1 default is an immutable imported Source with separately saved Notes/Annotations. If screenplay-text editing is required, decide its save/source-version contract before coding; do not store edits in `Work.version`.
- **MUST DECIDE NOW / CAN DEFER:** **CAN DEFER** Draft entity only if V1 screenplay text is read-only. **MUST DECIDE NOW** whether Writing Studio edits source text or only annotates it.

### Version

- **CONCEPT:** Source/Work Version.
- **WHERE IT APPEARS:** Narrative-model Work fields; Pydantic `Work.version`; feature map later Draft History/Comparison; screen map save ambiguity.
- **CURRENT REPRESENTATION:** A single optional string on Work; no immutable snapshots or version links.
- **PROBLEM:** Metadata label/version number does not provide a version history, source identity, annotation anchoring, or draft comparison.
- **V1 REQUIREMENT:** Stable identity for the imported Source used by evidence/annotations; full revision history is not required if V1 source is immutable.
- **PROPOSED RESOLUTION:** Keep `Work.version` as descriptive metadata only. Defer Version as a separate immutable snapshot entity until Draft History/Comparison is approved. If sources are replaced in V1, define new Source identity rather than overwriting silently.
- **MUST DECIDE NOW / CAN DEFER:** **CAN DEFER** version-history entity. **MUST DECIDE NOW** whether source replacement is allowed and how anchors remain valid.

### Themes, Motifs, Setups, Payoffs, and Conventions

- **CONCEPT:** Theme, Motif, Setup, Payoff, Convention.
- **WHERE IT APPEARS:** Narrative-model §§Theme/Motif/Setup/Payoff/Convention; feature map later themes/motifs/conventions and information/setup-payoff tracing.
- **CURRENT REPRESENTATION:** Conceptual entities in the architecture document; no Pydantic schemas. Feature map places their indexes/tracing later.
- **PROBLEM:** Their presence in the conceptual ontology can be misread as a V1 promise or as parser-extractable facts.
- **V1 REQUIREMENT:** V1 can link an explicitly curated Mechanism or claim where useful; it does not require standalone theme/motif/setup/payoff/convention inventories.
- **PROPOSED RESOLUTION:** Keep these as future entities. If a V1 analysis mentions one, represent it as a typed AnalysisClaim with Evidence, not as an automatically discovered canonical record.
- **MUST DECIDE NOW / CAN DEFER:** **CAN DEFER** entity schemas and dedicated views. **MUST DECIDE NOW** not to infer them automatically in V1.

## A. V1 CANONICAL OBJECT MODEL

This is the proposed classification for a V1 implementation contract. “Existing” describes the current conceptual/schema starting point; it does not mean implementation is complete.

### Narrative entities retained from the current model

- **Work** — canonical narrative container; same identity in Study and Make.
- **Character** — Work-scoped participant.
- **Scene** — ordered Work unit; add a stable link to its Source span.
- **Beat** — explicit change unit within a Scene; never equate it with a parser block.
- **Event** — story-world occurrence, distinct from app activity.
- **Relationship** — Work-scoped link between Character participants.
- **Objective** and **Obstacle** — existing entities linked to Character/Scene as specified.
- **Information** — Work-scoped item; V1 uses contextual links, not full knowledge-flow analysis.
- **Evidence** — source-support record; link it to Source and AnalysisClaim.
- **World** and **Location** — existing contextual entities when populated; no dedicated V1 global screens required.
- **Mechanism** — minimal canonical concept entity required by Work Page and Reference Shelf; separate concept identity from its occurrence/claim in a Scene.

### V1 source and claim objects to add explicitly

- **Source** — new domain entity identifying a source/representation for a Work and resolving to its original content/reference. Film and screenplay are Source kinds/representations by default.
- **AnalysisClaim** — proposed new entity for a claim attached to a narrative target, with status FACT / INFERENCE / INTERPRETATION and links to supporting Evidence. “Analysis” itself is a view/grouping of claims, not this entity.
- **Note/Material** — new user-generated freeform content, optionally linked to narrative objects.
- **Annotation** — new user-generated content anchored to a Scene and/or stable Source span; distinct from Evidence and freeform Note.
- **UserReference** — user-to-existing-object association for saved Works/Scenes/Mechanisms. Reference Shelf is a view over these associations.
- **Ownership relation** — system-level user-to-Work/Note/Annotation/Reference relation. It is not part of narrative ontology; exact User/account representation is an open persistence decision.

### V1 metadata, views, and derived information

- **Creator** — Work metadata string/list in V1, not a canonical entity.
- **Film / Screenplay** — Source representation kinds, not separate Work types by default.
- **Document** — stored/imported payload artifact behind Source, not a separate narrative entity in V1.
- **Narrative Anatomy, Character Study, Evidence view, Reference Shelf, Search, Work Page, Scene Study, Writing Studio** — contextual screens/views, not entities.
- **Analysis** — derived grouping/presentation of AnalysisClaims.
- **Interpretation** — one AnalysisClaim status, not an entity.
- **Narrative State** — V1 change/status claim attached to a target with Evidence; not a standalone typed state object.
- **ScriptBlock/parser classification** — derived parser output with a source span; not a Beat or canonical narrative entity.

## B. V1 DEFERRED OBJECTS

These concepts are present in the long-term model or product map but do not need a canonical V1 entity/view:

- **Structural Unit** — typed hierarchy of acts/movements/sequences; V1 ordered Scene index and explicitly supplied structural claims are sufficient.
- **Narrative State snapshot/trajectory** — typed state transitions and trajectory timelines.
- **StudyActivity / StudyRecord** — durable user Study History, separate from narrative Event.
- **Draft and Version** — editable screenplay draft/version snapshots and comparison; defer if V1 imported Source remains immutable.
- **Theme, Motif, Setup, Payoff, Convention** — dedicated indexes/tracing workflows.
- **Cross-work Character identity**, relationship/character trajectory, information-flow graph, full mechanism taxonomy/tracing, comparison graph, transform artifacts, and collaboration/share objects.
- **Creator entity** — canonical authority record, only if cross-work identity/roles become a requirement.
- **Document artifact entity** — only if a Source needs multiple independently addressable files/formats.

Deferred does not mean these ideas are removed from the conceptual architecture document; it means V1 must not imply their typed support or automatic discovery.

## C. V1 RELATIONSHIPS

The relationships below are the minimum proposed links implied by V1. “Existing” means a field/ID relation is present today; “needs definition” means product/schema work remains. This list does not prescribe database tables or API shape.

| From | Relationship | To | Current state / V1 note |
| --- | --- | --- | --- |
| User | owns/has private access to | Work | No User model or ownership field today; system-level decision required. |
| Work | has source representation(s) | Source | `Work.source` is currently a string; replace conceptually with explicit Source relation only after ontology approval. |
| Source | contains/resolves to | Original screenplay text or film reference | Stored payload is not a narrative entity; preserve source separately from parsed output. |
| Source | is parsed into | ScriptBlock/source spans | Parser outputs type/text only today; retain offsets/line mapping. ScriptBlock is derived output. |
| Work | contains | Scene | `Scene.work_id` exists; parser does not build Scenes. |
| Scene | spans | Source | Required by Scene Study/Evidence, absent today. Define stable start/end locators. |
| Work | has/associates | Character | `Character.work_id` exists; keep V1 identity Work-scoped. |
| Scene | involves | Character | `Scene.character_ids` exists; IDs are strings and need integrity rules. |
| Work | has | Relationship | `Relationship.work_id` exists. |
| Relationship | has participants | Character | Participant IDs exist as strings; require participants from the same Work in V1. |
| Scene | contains | Beat | `Beat.scene_id` exists; do not derive Beat from formatting blocks. |
| Character | pursues | Objective | `Objective.character_id` exists. |
| Scene | concerns/links | Objective and Obstacle | Scene ID lists exist; objective/obstacle interpretations need claim/evidence support. |
| Objective | is impeded by | Obstacle | `Obstacle.objective_id` exists. |
| Work | has | Event / Information | `Event.work_id` and `Information.work_id` exist. |
| Scene | references/introduces/reveals | Event / Information | Scene ID lists exist; timing/knowledge semantics are underspecified. |
| Event | involves | Character / Location | Participant/location IDs exist as strings/optional IDs; validate within Work. |
| Event | precedes/causes/consequences | Event | Causal ID lists exist; causal relation should remain distinct from chronology. |
| Scene/Character/Relationship/Mechanism | is target of | AnalysisClaim | New proposed relation. A claim must say what it analyzes. |
| AnalysisClaim | is supported by | Evidence | Proposed separation; current Evidence embeds a claim string. One claim may have multiple Evidence records. |
| Evidence | cites | Source span/location | Current `source_id`, page, line, text span are weakly linked/optional; stable source locator required. |
| Note | authored by | User | New user-generated object; privacy/owner model required. |
| Note | optionally references | Work / Scene / Character / Evidence | Use links without copying target objects; references are contextual, not ownership of the target. |
| Annotation | authored by | User | New user-generated object. |
| Annotation | anchors to | Scene and/or Source span | Required anchor; can link to an AnalysisClaim/Evidence, but is not itself proof. |
| UserReference | belongs to | User | New association record. |
| UserReference | points to | Work / Scene / Mechanism | Target remains canonical; Reference Shelf lists the association. |
| StudyActivity (later) | records user activity about | Work / Scene | Do not reuse narrative Event or UserReference. |
| Draft/Version (later) | derives from/versions | Work or Source | Requires immutable identity/lineage; do not overload `Work.version`. |

## D. OPEN PRODUCT DECISIONS

The audit makes proposed defaults for the six explicitly requested decisions. These additional choices still need product confirmation before dependent implementation:

| Decision | Proposed default from this audit | When to resolve |
| --- | --- | --- |
| Work ownership/authentication | V1 user Works, Notes, Annotations, and References must be private and owner-scoped. Whether this means accounts, local-only, or synced storage is not defined. | Before My Works/Notebook persistence. |
| Film/screenplay representation edge cases | One Work may have a Film Source and Screenplay Source; a materially distinct adaptation can be a separate Work by editorial decision. | Before adding works with multiple adaptations/screenplay drafts. |
| Source formats and locators | V1 needs a stable text-span/line strategy; current parser loses line/offset data. Accepted formats and page-vs-line requirements are unsettled. | Before parser/source intake implementation. |
| Analysis authorship and review | Proposed V1 uses curated human analysis, deterministic parser output, and user-authored notes; no automatic interpretation. Who authors/reviews curated claims remains open. | Before populating Story Atlas and Work Pages. |
| AnalysisClaim representation | Proposed separate AnalysisClaim from Evidence; decide claim target cardinality, status, and author/provenance. | Before Work/Scene analysis data is authored. |
| Mechanism semantics | Minimal V1 concept entity with explicit occurrence/claim links; taxonomy and who assigns it are unsettled. | Before mechanism tags appear in V1 catalog. |
| Note vs Annotation payload | Distinct concepts; decide whether Annotation owns text or references a Note, and whether one annotation can anchor multiple spans. | Before Scene Work/Notebook data contract. |
| Screenplay editing depth | Proposed safe V1 default is immutable imported Source plus editable Notes/Annotations. Feature map still asks for a “working screenplay environment”; actual text editing requires a source/version contract. | Before Writing Studio implementation. |
| Structural hierarchy | V1 uses Scene order and supplied claims; decide which acts/sequences are explicitly curated, if any, in the initial corpus. | Before loading structured Work data. |
| Reference Shelf navigation | This audit resolves Library as a V1 top-level destination. Confirm with product owner before navigation implementation. | Before navigation implementation. |
| Creator metadata | V1 creator names remain strings; confirm whether credits need role/type distinctions for the initial corpus. | Before corpus entry/import. |
| Source permissions and rights | Define which film references and screenplay texts can be stored/displayed and how source provenance is credited. | Before curating/publishing corpus content. |

### Explicit resolutions requested

1. **Creator:** Work metadata in V1; no Creator entity.
2. **Source/Document:** Source is a V1 entity; Document is a storage artifact behind Source, not a separate narrative entity in V1.
3. **Note vs Annotation:** Separate user-generated concepts. Note is freeform/optionally linked; Annotation requires a Scene/source-span anchor.
4. **Structural Unit:** Defer the typed entity; V1 uses ordered Scenes and contextual structure claims.
5. **Film vs Screenplay:** Default to one Work with separate Source representations/kinds. Use separate Work identities only for editorially distinct narrative works/adaptations.
6. **Library:** Keep Library top-level in V1 for personal Reference Shelf; Study opens Story Atlas. This resolves the earlier feature-map ambiguity for this architecture pass.

## E. CONCEPTS CODEX MUST NOT INVENT

- Do not create a Creator entity, Creator profile screen, or creator role ontology in V1; use Work metadata until explicitly revised.
- Do not equate Film, Screenplay, Work, Source, and Document, or create separate Work records solely because one source is a film and another is a screenplay.
- Do not infer that all film/screenplay adaptations share one Work; use the explicit editorial Work/source rule above.
- Do not treat parser `ScriptBlock` as Scene, Beat, Evidence, or AnalysisClaim.
- Do not infer characters, objectives, relationships, information knowledge, themes, motifs, mechanisms, setups/payoffs, or interpretations from capitalization/formatting alone.
- Do not invent a Structural Unit hierarchy or act/sequence boundaries from `Scene.sequence`.
- Do not treat `Scene.state_before`/`state_after` dictionaries as a validated Narrative State ontology.
- Do not conflate Note, Annotation, Evidence, AnalysisClaim, and Interpretation. They have different authorship, anchors, and evidentiary roles.
- Do not present an interpretation as FACT or treat a Note/Annotation as source evidence.
- Do not reuse narrative Event for user navigation, recent activity, or Study History.
- Do not duplicate a Work/Scene/Mechanism in Reference Shelf; save a UserReference to the canonical object.
- Do not treat `Work.version` as draft/version history or silently overwrite a Source while spans are referenced.
- Do not infer account ownership, cloud sync, sharing visibility, or data deletion semantics from the phrase “private.”
- Do not make Library/Reference Shelf a second copy of Story Atlas content.
- Do not add confidence scales, numeric relationship states, mechanism taxonomies, or cross-work identity rules without defining their source and meaning.

## Audit outcome

The current ontology provides a useful base for Work, Character, Scene, Beat, Event, Relationship, Objective, Obstacle, Information, and Evidence. The product architecture requires explicit V1 decisions for Source identity, source spans, AnalysisClaim/claim status, user ownership, Note, Annotation, UserReference, and minimal Mechanism identity. Structural Unit, typed Narrative State, history, Draft/Version, and the broader indexes/tracing features can remain future concepts.

The screen and feature maps should be treated as proposed product requirements, not proof that the existing Pydantic schemas or parser already support these relationships. This audit records the proposed resolutions in one place without silently changing any prior document.
