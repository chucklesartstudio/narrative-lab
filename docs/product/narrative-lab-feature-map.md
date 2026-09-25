# Narrative Lab Feature Architecture

## Purpose and status

This document is the product-level source of truth for Narrative Lab V1 and its later feature roadmap. It translates interaction patterns from [the Studio feature inventory](../design/studio-feature-inventory.md) into a film and screenplay product. It does not treat Studio screens as Narrative Lab's information architecture.

The map is conceptual product architecture. No screen design, API contract, implementation technology, or AI behavior is specified here.

## Product principle

Narrative Lab is a digital environment for **studying** existing narrative works and **making** a user's own narrative work. The initial medium is film/screenplay. Study and Make use the same underlying narrative objects and source/evidence relationships, so a user's screenplay can be explored with the same structures used to study an existing work.

The product should feel like an annotated film archive, screenplay desk, narrative research instrument, structural microscope, and writing environment. It should not feel like a chatbot, screenplay-template generator, course platform, generic SaaS dashboard, or productivity tracker.

The central V1 loop is:

```text
STUDY A SCREENPLAY
→ UNDERSTAND ITS STRUCTURE
→ EXPLORE SCENES
→ EXPLORE CHARACTERS
→ INSPECT NARRATIVE ANATOMY
→ TRACE EVIDENCE
→ MAKE NOTES
```

V1 should make that loop coherent for a deliberately bounded set of film/screenplay material and one user's own screenplay workflow. It should not attempt the full roadmap.

## Architecture rules for product features

1. A Work, Scene, Character, Relationship, Event, Beat, Objective, Obstacle, Information item, Narrative State, Theme, Motif, Setup, Payoff, Mechanism, Convention, or Evidence record has one identity that can appear in multiple contexts.
2. Study and Make are different working contexts over shared narrative objects. They must not fork into separate narrative models.
3. Keep source material distinct from parser output, analysis, evidence, and interpretation.
4. Every non-trivial analytical claim should be able to point to source evidence. Mark claims as **FACT**, **INFERENCE**, or **INTERPRETATION**; do not present interpretation as source fact.
5. V1 structural analysis should be inspectable and editable by a person. This map does not assume AI-generated interpretation.
6. Global navigation should expose work areas, not every narrative object. Move through objects contextually and provide a clear return path.
7. Desktop, tablet, and phone use the same product model. Only the arrangement and order of presentation change.

## Translation types and release labels

- **DIRECT:** the same interaction transfers with minimal change.
- **ADAPTED:** the interaction transfers, but its content or information architecture changes.
- **NEW:** Narrative Lab needs the capability and Studio has no equivalent interaction.
- **EXCLUDED:** an actor-specific or inappropriate Studio feature; not part of Narrative Lab.
- **V1:** required to demonstrate the central loop.
- **LATER:** valuable after V1 is coherent.
- **RESEARCH / EXPERIMENTAL:** a later capability whose analytical representation or user value needs validation. These are counted in the Later total.

Priorities are High, Medium, or Low. They indicate product importance, not a permission to implement outside the V1 boundary.

This map contains **30 proposed features**: **15 V1** and **15 Later** (including items marked Research / Experimental). It separately lists **13 excluded feature groups**.

## Proposed V1 feature catalogue

### V1-01 — Home

- **MODE:** Common entry into Study and Make.
- **PURPOSE:** Editorial starting point that returns a user to a meaningful work or study.
- **USER NEED:** Know what to explore or continue without facing a dashboard of utility buttons.
- **CORE USER ACTION:** Open a featured study, discover a work, resume a recent study, or continue a current work.
- **SYSTEM BEHAVIOR:** Curate entry points using available work records and the user's recent context; do not imply activity that is not stored.
- **INPUT:** Curated Study material and, when available, the user's current/recent work references.
- **OUTPUT:** Navigation to Story Atlas, Work Page, Scene Study, or a user's work.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Mechanism, Evidence; user work/reference relationships.
- **STUDIO ORIGIN:** Curated Home and featured Atlas item; Studio's Home content is static and actor-specific.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1.
- **DEPENDENCIES:** A small curated Work catalog; contextual navigation; persistence for genuine recent/current items.
- **RESPONSIVE:** **DESKTOP** editorial feature plus discovery and continue-work areas; **TABLET** reduced columns with one primary feature; **PHONE** stacked featured study, discovery, and continue-work sections.

### V1-02 — Story Atlas

- **MODE:** Study.
- **PURPOSE:** Curated, searchable archive of films and screenplays available to study.
- **USER NEED:** Find a work by relevant metadata and understand why it is in the archive.
- **CORE USER ACTION:** Browse, search, filter by supported metadata, and open a Work Page.
- **SYSTEM BEHAVIOR:** Return matching Works deterministically and show which filters are active; do not present inactive chips as working filters.
- **INPUT:** Query and explicit metadata facets such as title, creator, year, genre, medium, or period when populated.
- **OUTPUT:** Matching Work summaries and contextual links to their detail pages.
- **RELEVANT NARRATIVE OBJECTS:** Work, Creator, Scene, Mechanism, Convention.
- **STUDIO ORIGIN:** Performance Atlas archive, text search, and filter-chip presentation. Studio's search works; its filter chips do not affect results.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1.
- **DEPENDENCIES:** Curated catalog and reliable metadata; Work Page; deterministic search/filter behavior.
- **RESPONSIVE:** **DESKTOP** searchable results with visible facets and compact summaries; **TABLET** reduced facet row or drawer; **PHONE** stacked search, touch-friendly filters, and result cards.

### V1-03 — Work Page

- **MODE:** Study and Make, using the same Work identity.
- **PURPOSE:** Provide a complete but navigable analytical overview of one film/screenplay or user work.
- **USER NEED:** Understand what the work contains and reach its relevant scenes, characters, structure, relationships, information, mechanisms, and evidence.
- **CORE USER ACTION:** Review the work overview, then select a narrative object or section for deeper study.
- **SYSTEM BEHAVIOR:** Assemble linked summaries and counts from the shared narrative model; distinguish unavailable analysis from empty data.
- **INPUT:** Work metadata, source description, and linked narrative records.
- **OUTPUT:** Work overview and contextual navigation to scenes, characters, relationships, structural units, information, mechanisms, and evidence.
- **RELEVANT NARRATIVE OBJECTS:** Work, World, Scene, Character, Relationship, Event, Structural Unit, Information, Mechanism, Evidence.
- **STUDIO ORIGIN:** Atlas Entry's context-first editorial detail pattern; Studio does not model this narrative overview.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1.
- **DEPENDENCIES:** Shared Work identity; populated catalog/source; linked entities; Evidence records and claim status; Story Atlas and Scene Study.
- **RESPONSIVE:** **DESKTOP** overview alongside scene index and selected analysis; **TABLET** overview with collapsible sections/drawers; **PHONE** stacked sections with contextual drill-in and back navigation.

### V1-04 — Scene Study

- **MODE:** Study.
- **PURPOSE:** Inspect a source scene together with a concise, evidence-linked account of its narrative anatomy.
- **USER NEED:** Move from the screenplay passage to what changes in the scene and see the material behind each claim.
- **CORE USER ACTION:** Select a scene, read its screenplay text and metadata, inspect its characters/objectives/obstacles/information/change/function, then open supporting evidence.
- **SYSTEM BEHAVIOR:** Keep scene text primary; show linked analytical fields and source spans; allow navigation to connected characters and evidence.
- **INPUT:** A Work's screenplay/source, scene boundaries, metadata, analysis, and evidence links.
- **OUTPUT:** Scene view with source text, analysis, related objects, and return paths to Work.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Character, Objective, Obstacle, Information, Event, Beat, Narrative State, Evidence.
- **STUDIO ORIGIN:** Atlas Entry scene analysis and Script Lab concept. Studio's Script Lab has no implemented screenplay reading or annotation workflow.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1.
- **DEPENDENCIES:** Stable scene segmentation and source references; Work Page; narrative links; claim/evidence classification.
- **RESPONSIVE:** **DESKTOP** scene index + screenplay + anatomy/evidence panes; **TABLET** screenplay with one analysis drawer/split view; **PHONE** sequential scene → screenplay → anatomy → evidence, with touch-friendly contextual sheets.

### V1-05 — Character Study

- **MODE:** Study.
- **PURPOSE:** Explore one Character through their goals, appearances, relationships, knowledge, and observed changes in a Work.
- **USER NEED:** Follow a character through the source rather than rely on a detached biography or unsupported interpretation.
- **CORE USER ACTION:** Select a character from a Work/Scene and inspect linked scenes, objectives, relationships, information, and evidence.
- **SYSTEM BEHAVIOR:** Aggregate linked records in narrative order and label analysis by claim type; V1 shows basic state/appearance changes, not a full trajectory visualization.
- **INPUT:** Character record and linked scene/event/relationship/evidence records.
- **OUTPUT:** Character detail with contextual paths back to relevant scenes and claims.
- **RELEVANT NARRATIVE OBJECTS:** Character, Scene, Objective, Relationship, Event, Information, Narrative State, Evidence.
- **STUDIO ORIGIN:** Editorial detail-page pattern only; no character-study feature in Studio.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, basic linked study only.
- **DEPENDENCIES:** Character identity; Work and Scene links; evidence-backed analysis. Full trajectory tooling is later.
- **RESPONSIVE:** **DESKTOP** character summary and appearance/relationship lists beside selected context; **TABLET** tabbed/drawer sections; **PHONE** stacked summary and chronological scene links.

### V1-06 — Narrative Anatomy (basic)

- **MODE:** Study and Make.
- **PURPOSE:** Make the story's basic structural and causal organization inspectable without requiring an advanced graph.
- **USER NEED:** See how scenes, events, objectives, obstacles, information, and changes relate at a useful level.
- **CORE USER ACTION:** Move between ordered scenes and inspect each scene's selected linked narrative objects.
- **SYSTEM BEHAVIOR:** Present sequence, acts/structural units when supplied, scene function, basic causal predecessors/consequences, and linked scene anatomy. Do not invent structure when it has not been established.
- **INPUT:** Scene order, structural units, events, scene analysis, and explicit causal links.
- **OUTPUT:** Ordered structural index and contextual anatomy summaries.
- **RELEVANT NARRATIVE OBJECTS:** Work, Structural Unit, Scene, Event, Beat, Objective, Obstacle, Information, Narrative State, Mechanism.
- **STUDIO ORIGIN:** NEW; Studio's sectioned Atlas detail is an editorial presentation analogue, not a structural model.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, as an ordered/indexed view; graph exploration is later.
- **DEPENDENCIES:** Reliable scene order and entity links; populated/curated analysis; distinction between source fact and analytical claim.
- **RESPONSIVE:** **DESKTOP** ordered scene index and selected anatomy panel; **TABLET** split list/detail or drawer; **PHONE** ordered sections and scene-to-scene navigation without a dense graph.

### V1-07 — Evidence and Claim Status

- **MODE:** Study and Make.
- **PURPOSE:** Connect an analytical claim to its source and distinguish fact, inference, and interpretation.
- **USER NEED:** Check how an observation is supported and avoid presenting interpretation as fact.
- **CORE USER ACTION:** Open evidence attached to a claim; in Make, attach a source span to a note or basic annotation.
- **SYSTEM BEHAVIOR:** Show the source excerpt/location, linked claim, observation, and one of FACT / INFERENCE / INTERPRETATION. Preserve the exact claim/evidence relationship.
- **INPUT:** Source span/location and claim classification.
- **OUTPUT:** Inspectable evidence record and claim context.
- **RELEVANT NARRATIVE OBJECTS:** Evidence, Work/source, Scene, Beat, Character, Information, Note/Annotation.
- **STUDIO ORIGIN:** NEW; Studio Atlas presents context and image credits but no claim-level evidence records.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1.
- **DEPENDENCIES:** Stable source offsets/line references; Evidence link model; a claim-status field or equivalent. Existing schema has `Evidence` but not the fact/inference/interpretation classification.
- **RESPONSIVE:** **DESKTOP** evidence side panel next to source; **TABLET** sheet/drawer or split view; **PHONE** bottom sheet or sequential evidence view with a clear return to the claim.

### V1-08 — Search

- **MODE:** Common to Study and Make.
- **PURPOSE:** Find available Works and their indexed metadata from anywhere in the product.
- **USER NEED:** Reach a known work or narrative object without navigating every collection manually.
- **CORE USER ACTION:** Enter a query and optionally choose supported metadata filters.
- **SYSTEM BEHAVIOR:** Search only indexed/available fields, disclose matching scope, and return Work or contextual object results. V1 search does not claim semantic understanding.
- **INPUT:** Query; supported metadata such as work title, creator, year, genre, character, scene, or mechanism name when indexed.
- **OUTPUT:** Ranked/deterministic result list with destination context.
- **RELEVANT NARRATIVE OBJECTS:** Work, Character, Scene, Location, Mechanism, Theme, Motif, Reference.
- **STUDIO ORIGIN:** Atlas text-search interaction; its implementation only indexes actor, film, director, and tags.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, deterministic metadata search only.
- **DEPENDENCIES:** Searchable catalog and declared indexed fields; Work/scene links. No semantic search dependency.
- **RESPONSIVE:** **DESKTOP** global search with result scope/facets; **TABLET** overlay or dedicated results view; **PHONE** full-page query and stacked results.

### V1-09 — Reference Shelf

- **MODE:** Common, primarily Study.
- **PURPOSE:** Let a user retain a small collection of Works, Scenes, or Mechanisms for later study.
- **USER NEED:** Return to selected reference material without confusing personal saves with the public/curated Atlas.
- **CORE USER ACTION:** Save or remove a reference and open it from the Shelf.
- **SYSTEM BEHAVIOR:** Store references by shared object identity and return them to their original contextual detail. V1 has no public sharing.
- **INPUT:** User save/remove action on an available Work, Scene, or Mechanism.
- **OUTPUT:** Personal Reference Shelf and linked detail destinations.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Mechanism, UserReference.
- **STUDIO ORIGIN:** Practice Library browse pattern; Studio has no saved shelf behavior.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** V1, basic save/list/open only.
- **DEPENDENCIES:** Stable object IDs and user-scoped persistence; contextual navigation.
- **RESPONSIVE:** **DESKTOP** saved-object list with detail preview; **TABLET** list plus drawer; **PHONE** stacked saved items and touch-friendly save/remove controls.

### V1-10 — My Works and Source Intake

- **MODE:** Make.
- **PURPOSE:** Create a user's private Work record and provide source screenplay text to the shared narrative workflow.
- **USER NEED:** Bring a screenplay into Narrative Lab and return to it later.
- **CORE USER ACTION:** Create a Work and import/paste screenplay text; view intake/parse status.
- **SYSTEM BEHAVIOR:** Retain the original source, parse supported text into blocks/scenes, report unsupported or uncertain classification, and never silently substitute parsed output for the source.
- **INPUT:** Work metadata and V1 screenplay text. Proposed narrow default is plain text; accepted file types require a product decision.
- **OUTPUT:** User-owned Work, preserved source, parser output, and a navigable scene index when scene boundaries are available.
- **RELEVANT NARRATIVE OBJECTS:** Work, source/document, Scene, ScriptBlock, Evidence.
- **STUDIO ORIGIN:** NEW; Studio Script Lab's upload is inert.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, minimal intake for the central loop.
- **DEPENDENCIES:** User/work persistence; source version identity; parser that retains line/span provenance. Existing parser only classifies lines and does not create scenes.
- **RESPONSIVE:** **DESKTOP** works list and intake/source status; **TABLET** list with intake sheet; **PHONE** stacked works list and simplified text intake with clear progress.

### V1-11 — Writing Studio / Screenplay Lab

- **MODE:** Make.
- **PURPOSE:** Provide the main working context for the user's screenplay while using the same narrative model as Study.
- **USER NEED:** Read and work on their script without losing access to its scenes, characters, and linked analysis.
- **CORE USER ACTION:** Open a Work, read its screenplay, move to a scene, and inspect linked notes/anatomy.
- **SYSTEM BEHAVIOR:** Display original text and scene navigation with analysis that references the same Work/Scene/Character entities as Study. V1 does not imply a full professional screenplay editor or template generator.
- **INPUT:** User Work/source and its parsed/curated narrative records.
- **OUTPUT:** Persistent screenplay workspace and contextual links to Scene Work and Notebook material.
- **RELEVANT NARRATIVE OBJECTS:** Work, source/document, Scene, Character, Beat, Objective, Obstacle, Evidence, Note/Annotation.
- **STUDIO ORIGIN:** Script Lab's intended text-workspace idea; Studio's screen itself is a visual placeholder.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, read/navigate/annotate at a basic level; advanced editing is later.
- **DEPENDENCIES:** My Works/source intake; stable scene mapping; shared narrative model; notes and evidence linkage.
- **RESPONSIVE:** **DESKTOP** scene index + screenplay + analysis panes; **TABLET** screenplay plus one collapsible analysis pane; **PHONE** sequential scene index, screenplay, anatomy, and note views.

### V1-12 — Scene Work and Basic Annotations

- **MODE:** Make.
- **PURPOSE:** Attach a user's note or simple analytical tag to a scene or selected source span.
- **USER NEED:** Capture a question, observation, objective, obstacle, or change while working on the screenplay.
- **CORE USER ACTION:** Select a passage or scene, choose a basic annotation kind, and add/edit a note.
- **SYSTEM BEHAVIOR:** Anchor the note to a stable source span or Scene; show its type and link; preserve it separately from source text and from evidence-backed claims.
- **INPUT:** Scene/text selection, annotation kind, note text, optional evidence/source reference.
- **OUTPUT:** Persistent basic annotation visible in Scene Work and the source context.
- **RELEVANT NARRATIVE OBJECTS:** Scene, Beat, Objective, Obstacle, Information, Evidence, Note/Annotation.
- **STUDIO ORIGIN:** Script Lab copy mentions beat/objective annotations and comments but no working annotation behavior exists; underlying feature is new to Narrative Lab.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1, basic private notes/tags only.
- **DEPENDENCIES:** Stable source spans; user/work persistence; explicit separation of authored notes from source facts and analytical claims.
- **RESPONSIVE:** **DESKTOP** inline selection with annotation side panel; **TABLET** selection opens a sheet/drawer; **PHONE** touch selection with bottom-sheet annotation editor.

### V1-13 — Writer's Notebook

- **MODE:** Make, available as a common private workspace.
- **PURPOSE:** Capture and retrieve a user's observations, ideas, material, questions, fragments, and research notes.
- **USER NEED:** Keep raw creative/research material without forcing it into a screenplay scene or public feed.
- **CORE USER ACTION:** Create, edit, tag, and optionally link a private note to a Work, Scene, Character, or Reference.
- **SYSTEM BEHAVIOR:** Save notes privately, preserve their authored wording, and support later retrieval. Do not convert a note into a narrative fact automatically.
- **INPUT:** Text, optional tags, and optional links to existing narrative objects.
- **OUTPUT:** Private Note/Material record and links back to related context.
- **RELEVANT NARRATIVE OBJECTS:** Note/Material (new object), Work, Scene, Character, Evidence/Reference.
- **STUDIO ORIGIN:** Observation Journal's prompt and inline composer; Studio Save currently does not persist entries.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** V1, private text notes and links only; media capture/organization is later.
- **DEPENDENCIES:** Private user-scoped persistence; Note/Material entity; contextual links.
- **RESPONSIVE:** **DESKTOP** note list and editor/context pane; **TABLET** split view or editor sheet; **PHONE** single-column note list/editor with touch-friendly controls.

### V1-14 — Shared Narrative Model

- **MODE:** Shared by Study and Make.
- **PURPOSE:** Ensure curated works and user works can be analyzed and linked through one set of narrative object types.
- **USER NEED:** Move the same concepts between study, writing, evidence, and revision without duplicate records or incompatible labels.
- **CORE USER ACTION:** Use an object in any context and follow its links to related objects.
- **SYSTEM BEHAVIOR:** Keep canonical IDs and typed links; track source/provenance and distinguish source content, parser output, user note, and analytical claim.
- **INPUT:** Source material and authored/curated narrative records.
- **OUTPUT:** Reusable linked objects surfaced by Work Page, Scene Study, Writing Studio, Search, and Reference Shelf.
- **RELEVANT NARRATIVE OBJECTS:** Existing model objects plus proposed Note/Material, Source/Document, and claim classification.
- **STUDIO ORIGIN:** NEW; Studio's actor data model does not provide a narrative ontology.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1 foundation.
- **DEPENDENCIES:** Reconcile `docs/architecture/narrative-model.md` with backend schemas. Current schemas omit several documented concepts (including Theme, Motif, Setup, Payoff, Mechanism, Convention, and Structural Unit); the Evidence schema has no FACT/INFERENCE/INTERPRETATION field. This map does not change those schemas.
- **RESPONSIVE:** **DESKTOP**, **TABLET**, and **PHONE** share the same IDs, relationships, provenance, and permissions; only object presentation and navigation change.

### V1-15 — Contextual Navigation and Responsive Workspace

- **MODE:** Common to Study and Make.
- **PURPOSE:** Let users move among work contexts and narrative objects while retaining a clear parent and return path.
- **USER NEED:** Understand where they are in the Work → Scene → Character/Relationship → Information/Mechanism → Evidence hierarchy.
- **CORE USER ACTION:** Open a linked object and return to the prior context or selected work.
- **SYSTEM BEHAVIOR:** Keep context while drilling into an object; expose a small number of top-level areas; adapt pane arrangement to screen size without changing data architecture.
- **INPUT:** Current mode, selected Work/object, navigation history.
- **OUTPUT:** Contextual views with predictable back/return behavior.
- **RELEVANT NARRATIVE OBJECTS:** All navigable narrative objects; navigation state is presentation state, not a duplicate narrative record.
- **STUDIO ORIGIN:** Studio's local push/pop/fade navigation and contextual back labels; its five-tab bar and 430px constraint are not carried over.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** High.
- **V1 / LATER / EXCLUDED:** V1 foundation.
- **DEPENDENCIES:** Shared object identity, links, and user/work permission model.
- **RESPONSIVE:** **DESKTOP** top-level navigation plus contextual panes; **TABLET** fewer panes, drawers, sheets, and split views; **PHONE** sequential navigation, stacked sections, bottom sheets, and touch-sized controls.

## V1 priority table

All rows below are V1 because they directly support the requested central loop or one of its explicitly required entry/persistence capabilities. “High” and “Medium” distinguish core loop dependencies from supporting features; neither means all detail must be deep in V1.

| FEATURE | V1? | WHY | DEPENDENCIES | NOTES |
| --- | --- | --- | --- | --- |
| Home | Yes | Gives the user a clear entry into a study or current work. | Curated Work; navigation; recent context when available. | Editorial, not dashboard metrics. |
| Story Atlas | Yes | Provides the existing screenplay/work to study. | Curated catalog, metadata, Work Page. | Keep V1 corpus bounded. |
| Work Page | Yes | Hosts the loop's structural overview and links. | Shared model; Work, Scene, Character, Relationship, Information, Mechanism, Evidence. | Overview can be concise; no advanced graph. |
| Scene Study | Yes | Makes scene text and analysis inspectable together. | Source-preserving parser/scene boundaries; Evidence; linked entities. | Screenplay remains primary. |
| Character Study | Yes | Explicitly required by the study loop. | Character-to-scene/event/relationship links and evidence. | Basic appearances/state only; trajectory visualization later. |
| Narrative Anatomy (basic) | Yes | Lets users understand order, function, and change. | Scene order, structural units when known, basic causal links. | Ordered index/context, not graph exploration. |
| Evidence and Claim Status | Yes | Completes traceability and prevents interpretation being presented as fact. | Stable source positions; Evidence links; claim-type distinction. | This is an architecture dependency, not an AI feature. |
| Search | Yes | Supports discovery across available works and metadata. | Catalog and indexed fields. | Deterministic only. |
| Reference Shelf | Yes | Allows a user to retain works/scenes/mechanisms for the study loop. | Stable IDs and user-scoped persistence. | Save/list/open only. |
| My Works / Source Intake | Yes | Provides the user's work for the Make half of the loop. | Work ownership, source storage, parser/scene mapping. | Accepted formats and hosting policy remain decisions. |
| Writing Studio / Screenplay Lab | Yes | Gives a user a working screenplay context on the same model. | My Works, scenes, shared model, notes/annotations. | Not a template generator or full professional editor. |
| Scene Work / Basic Annotations | Yes | Turns screenplay reading into useful user notes at scene/span level. | Stable source spans, persistence, Note/Annotation model. | Keep notes separate from source and claims. |
| Writer's Notebook | Yes | Supports “make notes” and private material capture. | Private persistence, Note/Material, optional object links. | Text-first V1. |
| Shared Narrative Model | Yes | Enables Study/Make reuse instead of duplicate concepts. | Model/schema reconciliation and provenance. | Must be defined before features are built against it. |
| Contextual Navigation / Responsive Workspace | Yes | Makes the loop and object hierarchy navigable on all devices. | Stable links, navigation context, responsive presentation. | Four proposed top-level destinations; details below. |

## Study hierarchy

Study is organized around a Work, not a permanent tab for every object:

```text
STUDY
├── Story Atlas
│   └── Works
│       └── Work Page
│           ├── Structure / scene index
│           ├── Scene Study
│           │   ├── Characters
│           │   ├── Relationships
│           │   ├── Objectives / obstacles / change
│           │   ├── Information
│           │   ├── Mechanisms
│           │   └── Evidence
│           └── Character Study
└── Reference Shelf
```

Relationships, structure, information, mechanisms, themes, and motifs can first appear as contextual sections or linked views in a Work. They need not all become global navigation destinations. V1 supports basic Relationship, Information, and Mechanism summaries where the source/analysis exists; trajectory, graph tracing, and thematic indexes are later.

## Make hierarchy

Make is a connected writing workflow, not a set of unrelated tools:

```text
MAKE
├── My Works
│   └── Writing Studio / Screenplay Lab
│       ├── Scene Work
│       ├── Drafts (LATER: version history)
│       └── Revision (LATER: comparison/change tools)
├── Writer's Notebook / Material
└── Transform / Combine Material (LATER)
```

**My Works** owns the user's Work and source material. **Writing Studio** opens that Work and presents its screenplay against the shared narrative model. **Scene Work** adds context-linked notes/annotations to scenes or source spans. **Drafts** become meaningful when version history is added. **Revision** can compare and trace changes later. **Transform** and **Combine Material** are later creative operations whose semantics and user control need research; they do not generate replacement screenplays in V1.

## Later roadmap

The Later features deepen analysis or writing after the basic study/write/trace/note loop is working. The order is dependency-led, not a commitment to build every item.

### LATER-01 — Guided Study Session

- **MODE:** Study.
- **PURPOSE:** Offer an optional structured reading path through a scene.
- **USER NEED:** Learn to observe, make a hypothesis, inspect evidence, compare, and record a note without gamification.
- **CORE USER ACTION:** Follow a prompt sequence and optionally record an observation.
- **SYSTEM BEHAVIOR:** Present prompts, reveal/contextualize material, and link the resulting note to the scene.
- **INPUT:** Selected Work/Scene and prompt sequence.
- **OUTPUT:** Study session state and optional linked note.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Evidence, Note/Material.
- **STUDIO ORIGIN:** Daily Practice's gated sequence/completion feedback; its actor exercises are excluded.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Scene Study, evidence links, Notebook; session persistence if resumable.
- **RESPONSIVE:** **DESKTOP** source and prompt side by side; **TABLET** split view or drawer; **PHONE** sequential prompts and bottom-sheet evidence.

### LATER-02 — Narrative Knowledge / Mechanism Library

- **MODE:** Study.
- **PURPOSE:** Browse reusable narrative concepts, mechanisms, examples, and references.
- **USER NEED:** Understand a mechanism across works without treating it as a prescriptive formula.
- **CORE USER ACTION:** Browse/search a mechanism/topic and open linked Work/Scene examples.
- **SYSTEM BEHAVIOR:** Present definitions, variants, examples, counterexamples, and links to source evidence.
- **INPUT:** Curated Mechanism/Convention records and indexed examples.
- **OUTPUT:** Mechanism detail and cross-links to Works, Scenes, and evidence.
- **RELEVANT NARRATIVE OBJECTS:** Mechanism, Convention, Theme, Motif, Work, Scene, Evidence.
- **STUDIO ORIGIN:** Practice Library and craft-category browsing; actor course/exercise content does not transfer.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Shared model, curated knowledge corpus, search, Work/Scene evidence links.
- **RESPONSIVE:** **DESKTOP** topic index and example/detail panes; **TABLET** index with drawer; **PHONE** searchable topic list and stacked detail.

### LATER-03 — Character Trajectory

- **MODE:** Study and Make.
- **PURPOSE:** Trace change in a character's desire, belief, knowledge, commitment, or state over narrative time.
- **USER NEED:** See how a character changes and which scenes provide evidence for that change.
- **CORE USER ACTION:** Select a character and inspect/adjust a timeline of state changes.
- **SYSTEM BEHAVIOR:** Order changes by scene/event and link each claim to evidence; allow uncertainty and alternate interpretations.
- **INPUT:** Character state observations, narrative ordering, and evidence.
- **OUTPUT:** Character trajectory view.
- **RELEVANT NARRATIVE OBJECTS:** Character, Narrative State, Scene, Event, Objective, Information, Evidence.
- **STUDIO ORIGIN:** None; new narrative analysis capability.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium; research/experimental representation.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Character Study, typed state changes, chronological/narrative ordering, evidence model.
- **RESPONSIVE:** **DESKTOP** timeline and evidence detail; **TABLET** simplified timeline with drawer; **PHONE** ordered change list with one event open at a time.

### LATER-04 — Relationship Trajectory

- **MODE:** Study and Make.
- **PURPOSE:** Trace how a relationship changes across scenes and events.
- **USER NEED:** Understand shifts in trust, power, dependency, intimacy, hostility, or knowledge with supporting evidence.
- **CORE USER ACTION:** Select a pair/group of characters and inspect changes over the Work.
- **SYSTEM BEHAVIOR:** Present sourced state observations over time; avoid reducing complex relationships to unsupported numeric scores.
- **INPUT:** Relationship records, scene/event order, state observations, evidence.
- **OUTPUT:** Relationship history/trajectory with links to relevant scenes.
- **RELEVANT NARRATIVE OBJECTS:** Relationship, Character, Scene, Event, Narrative State, Information, Evidence.
- **STUDIO ORIGIN:** None; new narrative analysis capability.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium; research/experimental representation.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Character and Relationship links; evidence-backed state changes; temporal ordering.
- **RESPONSIVE:** **DESKTOP** trajectory plus scene/evidence panel; **TABLET** simplified trajectory and drawer; **PHONE** chronological list with relationship context in stacked sections.

### LATER-05 — Information Flow and Setup / Payoff Tracing

- **MODE:** Study and Make.
- **PURPOSE:** Trace when information is introduced, known, hidden, misunderstood, revealed, and later recontextualized; connect setups to payoffs.
- **USER NEED:** Understand audience/character knowledge and delayed meaning across a Work.
- **CORE USER ACTION:** Follow an Information item or Setup to its introduction, knowledge changes, reveal, and linked payoff.
- **SYSTEM BEHAVIOR:** Display explicit knowledge and reference links with source evidence; do not infer who knows what without a claim/source.
- **INPUT:** Information and Setup/Payoff links with scene/event positions.
- **OUTPUT:** Information path and setup/payoff chain.
- **RELEVANT NARRATIVE OBJECTS:** Information, Setup, Payoff, Character, Scene, Event, Evidence.
- **STUDIO ORIGIN:** None; no information-flow or payoff tracing in Studio.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** High after V1; research the representation.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Information and Setup/Payoff schema; event order; character knowledge; stable evidence links.
- **RESPONSIVE:** **DESKTOP** flow/timeline and evidence panel; **TABLET** reduced flow with detail drawer; **PHONE** stepwise chain/list with expandable evidence.

### LATER-06 — Narrative Graph, Scene Relations, and Dependency Tracing

- **MODE:** Study and Make.
- **PURPOSE:** Explore explicit relationships among scenes, events, causes, consequences, echoes, and dependent narrative elements.
- **USER NEED:** See how a local scene participates in wider structure without losing the source path.
- **CORE USER ACTION:** Select an object/link and traverse incoming/outgoing relationships.
- **SYSTEM BEHAVIOR:** Show typed, inspectable links; retain the selected Work/Scene context; let users return to source/evidence.
- **INPUT:** Explicit causal, chronological, structural, setup/payoff, or other typed links.
- **OUTPUT:** Filterable graph and an accessible list/path representation.
- **RELEVANT NARRATIVE OBJECTS:** Work, Structural Unit, Scene, Event, Beat, Objective, Information, Setup, Payoff, Mechanism, Evidence.
- **STUDIO ORIGIN:** None; Studio does not provide cross-linked narrative objects.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium; research/experimental.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Typed relationship model, meaningful link density, evidence/provenance, and non-graph navigation fallback.
- **RESPONSIVE:** **DESKTOP** graph with adjacent detail; **TABLET** filtered graph/list and drawer; **PHONE** list/path traversal rather than a shrunken graph.

### LATER-07 — Mechanism Tracing

- **MODE:** Study and Make.
- **PURPOSE:** Follow a mechanism's use, variation, escalation, reversal, or payoff within and across works.
- **USER NEED:** Compare how a narrative method produces an effect in different contexts.
- **CORE USER ACTION:** Open a mechanism and traverse linked Work/Scene examples and evidence.
- **SYSTEM BEHAVIOR:** Organize examples by explicit occurrence and interpretation, distinguishing a tagged pattern from a proven fact.
- **INPUT:** Mechanism records, scene/work links, claims, and source evidence.
- **OUTPUT:** Mechanism detail with traceable examples and variants.
- **RELEVANT NARRATIVE OBJECTS:** Mechanism, Work, Scene, Beat, Event, Evidence, Convention.
- **STUDIO ORIGIN:** Atlas/craft-category browsing as presentation pattern; mechanism itself is Narrative Lab-specific.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Narrative Knowledge Library; typed mechanism links; evidence; cross-work search.
- **RESPONSIVE:** **DESKTOP** mechanism entry beside examples; **TABLET** examples with detail drawer; **PHONE** stacked definition, examples, and source links.

### LATER-08 — Comparison Workspace / Structural Comparison

- **MODE:** Study and Make.
- **PURPOSE:** Compare two or more scenes/works/structures to identify similarity, contrast, and transformation.
- **USER NEED:** Examine narrative choices across examples without flattening differences or losing evidence.
- **CORE USER ACTION:** Select items and choose an aligned comparison dimension.
- **SYSTEM BEHAVIOR:** Align sources/structures where possible and show evidence for comparison claims; do not assert equivalence from metadata alone.
- **INPUT:** Selected Works/Scenes/structural units and comparison criteria.
- **OUTPUT:** Side-by-side or sequential comparison with links to original contexts.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Character, Mechanism, Structural Unit, Evidence, Note.
- **STUDIO ORIGIN:** None; Studio archive has no compare interaction.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Search/Atlas, stable scene order, shared model, source/evidence links.
- **RESPONSIVE:** **DESKTOP** simultaneous comparison panes; **TABLET** split or swipeable panels; **PHONE** switch between comparison sides with a persistent comparison context.

### LATER-09 — Themes, Motifs, and Conventions Index

- **MODE:** Study and Make.
- **PURPOSE:** Trace recurring conceptual questions, images, actions, or formal conventions across a Work or corpus.
- **USER NEED:** Connect repetition and variation to concrete appearances in the source.
- **CORE USER ACTION:** Open an item and inspect appearances, variations, related objects, and evidence.
- **SYSTEM BEHAVIOR:** Display only explicitly linked or reviewed appearances; distinguish descriptive recurrence from interpretation.
- **INPUT:** Theme/Motif/Convention records and Work/Scene/character/event associations.
- **OUTPUT:** Contextual index with source-linked appearances.
- **RELEVANT NARRATIVE OBJECTS:** Theme, Motif, Convention, Work, Scene, Character, Event, Evidence.
- **STUDIO ORIGIN:** Craft categories as browsing presentation only; these narrative concepts are new.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Model support, curated/annotated appearances, evidence and search.
- **RESPONSIVE:** **DESKTOP** index with appearance panel; **TABLET** reduced list and drawer; **PHONE** stacked concept detail and chronological appearance list.

### LATER-10 — Transformation Workspace

- **MODE:** Make.
- **PURPOSE:** Explore a deliberate transformation of a user's narrative material while preserving its source and lineage.
- **USER NEED:** Try structural or formal change without losing the original or confusing experiment with canon.
- **CORE USER ACTION:** Choose source material and a transformation operation, then review and accept/reject a proposed change.
- **SYSTEM BEHAVIOR:** Keep original and transformed versions distinct, record links and user choices, and require explicit user control. No automatic screenplay generation is assumed.
- **INPUT:** Selected Work/Scene/Mechanism and a user-defined transformation brief.
- **OUTPUT:** A linked experimental artifact and provenance/change record.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Beat, Mechanism, Structural Unit, Draft, Evidence, Note.
- **STUDIO ORIGIN:** None; no transformation workflow in Studio.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Low until its method and use are researched.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Draft/version lineage, source preservation, user-authored operation rules, clear experiment/canon distinction.
- **RESPONSIVE:** **DESKTOP** source and experiment side by side; **TABLET** reduced comparison with drawers; **PHONE** sequential source → operation → review, without dense multi-pane editing.

### LATER-11 — Draft History and Comparison

- **MODE:** Make.
- **PURPOSE:** Preserve screenplay revisions and compare chosen versions.
- **USER NEED:** Understand what changed and retain recoverable earlier work.
- **CORE USER ACTION:** Save/select versions and compare two versions or selected scenes.
- **SYSTEM BEHAVIOR:** Preserve immutable version snapshots or an equivalent history; surface text and linked narrative changes without overwriting source provenance.
- **INPUT:** User screenplay edits and selected version pair.
- **OUTPUT:** Version history and a comparison view.
- **RELEVANT NARRATIVE OBJECTS:** Work, Draft/Version, Scene, source spans, Note, Evidence.
- **STUDIO ORIGIN:** Static Recent Takes display suggests a history presentation, but Studio has no saved draft-version system.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium after basic writing is established.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Persistent drafts, stable scene mapping across revisions, diff strategy, lineage.
- **RESPONSIVE:** **DESKTOP** version list plus side-by-side diff; **TABLET** split or switchable comparison; **PHONE** sequential versions with inline change navigation.

### LATER-12 — Revision Tools

- **MODE:** Make.
- **PURPOSE:** Help a user inspect and organize revision work against scenes, objectives, mechanisms, and notes.
- **USER NEED:** Turn an observed structural issue or intention into a deliberate, traceable revision.
- **CORE USER ACTION:** Create a revision question/task linked to a source scene and mark its disposition.
- **SYSTEM BEHAVIOR:** Preserve user-authored revision intent and link resulting changes to relevant versions/scenes.
- **INPUT:** User note, selected scene/object, and later version changes.
- **OUTPUT:** Revision record and links to changed material.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Objective, Obstacle, Mechanism, Note, Draft/Version, Evidence.
- **STUDIO ORIGIN:** Journal capture and profile history as weak analogues; no revision workflow in Studio.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Medium after Draft History.
- **V1 / LATER / EXCLUDED:** LATER.
- **DEPENDENCIES:** Writing Studio, Notebook/Notes, Draft History, object links.
- **RESPONSIVE:** **DESKTOP** revision queue beside selected text; **TABLET** queue with scene drawer; **PHONE** prioritized list and focused revision detail.

### LATER-13 — Combine Material

- **MODE:** Make.
- **PURPOSE:** Bring selected notes, fragments, scenes, or references into a deliberate new working composition.
- **USER NEED:** Reuse accumulated material without losing provenance or accidentally merging source records.
- **CORE USER ACTION:** Select items, arrange them, and create a new linked work/artifact.
- **SYSTEM BEHAVIOR:** Preserve each source link and make the new artifact distinct from its source items.
- **INPUT:** Selected Notebook items, references, or user-work fragments.
- **OUTPUT:** New composition/artifact with provenance links.
- **RELEVANT NARRATIVE OBJECTS:** Note/Material, Work, Scene, Source, Reference, Draft.
- **STUDIO ORIGIN:** None.
- **TRANSLATION TYPE:** NEW.
- **PRIORITY:** Low until use cases are tested.
- **V1 / LATER / EXCLUDED:** LATER — RESEARCH / EXPERIMENTAL.
- **DEPENDENCIES:** Notebook, My Works, provenance, permissions, explicit user confirmation of resulting artifact.
- **RESPONSIVE:** **DESKTOP** multi-item board and output pane; **TABLET** selectable list with arrangement sheet; **PHONE** sequential item selection and composition review.

### LATER-14 — Work / Study History

- **MODE:** Common.
- **PURPOSE:** Provide a reliable archive of studied works, current context, saved references, and authored/revised work.
- **USER NEED:** Resume activity and retrieve work without relying on gamified progress metrics.
- **CORE USER ACTION:** Browse recent/current works and return to a saved study or draft.
- **SYSTEM BEHAVIOR:** Record meaningful user actions with context and provide resume destinations; do not use streaks or scores.
- **INPUT:** Saved Works, study activity, versions, and reference events.
- **OUTPUT:** Personal history/archive and Continue destinations.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Study record, Draft/Version, Reference.
- **STUDIO ORIGIN:** Profile / Artistic Record and Recent Takes, both static examples in Studio.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** Medium.
- **V1 / LATER / EXCLUDED:** LATER; V1 Home may show current work only when persistence supports it.
- **DEPENDENCIES:** User identity/privacy decision and durable activity/work records.
- **RESPONSIVE:** **DESKTOP** searchable/filterable history list; **TABLET** list and detail drawer; **PHONE** chronological stack with resume actions.

### LATER-15 — Discussion / Sharing

- **MODE:** Common to Study and Make.
- **PURPOSE:** Allow a user to share or discuss selected discoveries/material when collaboration is deliberately scoped.
- **USER NEED:** Exchange a reference or analysis with another person without turning private writing into a social feed.
- **CORE USER ACTION:** Explicitly share a selected item or invite discussion in a defined context.
- **SYSTEM BEHAVIOR:** Enforce clear visibility/ownership and show the shared source/context; no follower ranking or engagement metrics.
- **INPUT:** User-selected Work/Scene/Note and audience/permission.
- **OUTPUT:** Shared reference/discussion object with provenance and visibility controls.
- **RELEVANT NARRATIVE OBJECTS:** Work, Scene, Evidence, Note/Material, Share/Discussion.
- **STUDIO ORIGIN:** Community screen is static; no actual posting/comment behavior transfers.
- **TRANSLATION TYPE:** ADAPTED.
- **PRIORITY:** Low; not part of the core product loop.
- **V1 / LATER / EXCLUDED:** LATER, only after privacy and collaboration needs are established.
- **DEPENDENCIES:** Identity, permissions, moderation, privacy model, explicit sharing states.
- **RESPONSIVE:** **DESKTOP** contextual discussion beside shared material; **TABLET** drawer/sheet; **PHONE** sequential thread and source context with clear visibility controls.

## V1 scope and priority

V1 is the 15 features V1-01 through V1-15. The loop-critical center is Work Page → Scene Study → Character Study/Narrative Anatomy → Evidence → Note. Home, Atlas, Search, and Reference Shelf provide entry and retrieval; My Works and Writing Studio make the same loop available for a user's screenplay.

V1 excludes advanced graph traversal, full character/relationship trajectories, broad cross-work comparison, setup/payoff networks, automatic interpretation, and social/collaborative systems. Include only enough structural links and summaries to make the loop understandable.

## Navigation model

Proposed top-level destinations:

1. **Home** — editorial entry and genuine continue-work context.
2. **Study** — Story Atlas and contextual Work/Scene/Character exploration.
3. **Make** — My Works, Writing Studio, Scene Work, and Notebook entry points.
4. **Library** — personal Reference Shelf, distinct from the curated Story Atlas.

Search is a global action, not a fifth mode. Characters, relationships, information, mechanisms, structure, and evidence are generally reached within a Work/Scene context rather than given permanent global tabs.

Context path:

```text
WORK
→ SCENE
→ CHARACTER / RELATIONSHIP
→ INFORMATION / MECHANISM
→ EVIDENCE
→ return to the originating scene or work
```

The same path must work from Study or Make. A Scene reached from a Character should retain that Character as a return context.

## Responsive product rule

The narrative model, object identity, permissions, and feature behavior remain the same at every width.

- **DESKTOP:** use multi-pane analysis where it adds value; for scene work, show scene index, screenplay, and analysis/evidence together.
- **TABLET:** show fewer simultaneous panes; use split views, drawers, and sheets to expose context without crowding.
- **PHONE:** use sequential navigation, stacked sections, touch-sized controls, and bottom sheets for contextual detail. Keep screenplay text readable; do not squeeze a desktop three-column workspace onto a phone.

Feature cards above specify the responsive presentation for each area.

## Dependencies and known architecture gaps

The current repository is a scaffold, not an implementation of this map. The frontend is still the Next.js starter page; the FastAPI backend exposes only status/demo routes; the screenplay parser classifies lines into blocks but does not create scenes; and there is no persistence configuration.

Before implementation, resolve these dependencies:

- **Model reconciliation:** `docs/architecture/narrative-model.md` describes Narrative State, Theme, Motif, Setup, Payoff, Mechanism, Convention, and Structural Unit, while current Pydantic schemas do not define all of them. The model also needs explicit Source/Document and Note/Material provenance for the proposed workflows.
- **Claim status:** current `Evidence` has source, line/page, text span, claim, observation, and confidence, but does not classify a claim as FACT / INFERENCE / INTERPRETATION.
- **Source stability:** current `ScriptBlock` contains only type/text. Evidence and annotations need stable source offsets/line references, and parser output must preserve the original screenplay.
- **Scene segmentation:** current parser classifies lines only; it does not assemble scenes, beats, or character/objective links.
- **Persistence and privacy:** Reference Shelf, My Works, annotations, and the private Notebook require durable user-scoped storage. Whether V1 is local-only, account-backed, or cloud-synced is undecided.
- **Corpus and provenance:** Atlas content needs a defined source, editorial process, and rights policy. Screenplay text access may differ from film/work metadata.
- **Analysis authorship:** decide who creates Work/Scene analyses and how they are reviewed. The V1 default proposed here is curated/human-authored analysis plus deterministic parser output; no AI analysis is included.
- **Import scope:** decide accepted input format, size limits, and whether V1 supports paste/plain-text only or additional screenplay formats. This map recommends the smallest source intake capable of testing the loop; it does not claim existing parser support is production-ready.
- **Canonical work/source unit:** clarify whether a film and its screenplay are one Work with multiple Sources or linked Work records. The shared model should preserve both distinctions.
- **Meaning of Transform/Combine Material:** define user intent, output type, lineage, and control before implementation; both remain research/experimental.
- **Top-level naming:** this proposal uses Home, Study, Make, and Library. Validate whether Library deserves a top-level destination or belongs within Study/Make.

These are product/data decisions, not reasons to add AI, APIs, or infrastructure in this documentation task.

## Explicitly excluded from Narrative Lab V1

These are 13 excluded feature groups. They are not candidate Studio-to-Narrative features; the reason is actor-training specificity, social/product mismatch, or gamification.

| FEATURE | MODE | PURPOSE / USER NEED | STUDIO ORIGIN | TRANSLATION TYPE | V1 / LATER / EXCLUDED | PRIORITY | DEPENDENCIES / RESPONSIVE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Acting exercises | Excluded | Rehearse acting technique; not the narrative-study loop. | Daily Practice/Craft exercises | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Voice training | Excluded | Train vocal production. | Voice Studio | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Movement training | Excluded | Train actor movement. | Practice/Craft categories | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Self-tape recording | Excluded | Record actor auditions/performance. | Self-Tape Studio | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Teacher dashboards | Excluded | Administer/review actor training. | No Teacher Studio exists in source. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Student management | Excluded | Manage acting-school students. | Onboarding/profile implications only; no workflow. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Attendance | Excluded | Track school/class attendance. | Not implemented in supplied source. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Actor performance evaluation | Excluded | Score/evaluate an actor's performance. | Profile/teacher-review copy is static. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| XP | Excluded | Reward repeated app engagement. | Not implemented; prohibited product pattern. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Levels | Excluded | Gamified progression. | Not implemented; prohibited product pattern. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Badges | Excluded | Gamified achievement display. | Not implemented; prohibited product pattern. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Streak gamification | Excluded | Reward practice streaks. | Home/profile mock streak values. | EXCLUDED | EXCLUDED | None | None; no responsive design. |
| Social follower metrics | Excluded | Rank social reach/popularity. | Community has no metrics; explicitly excluded. | EXCLUDED | EXCLUDED | None | None; no responsive design. |

## Important product ambiguities to resolve

The feature map makes a proposed V1 boundary, but these decisions affect data and scope:

1. **Source format and ownership:** Is V1 import plain text only, and are uploaded sources local/private or account-backed/synced?
2. **Film vs screenplay identity:** Is a film and screenplay one Work with multiple Sources, or separate linked Works?
3. **Corpus:** Which works and screenplays can be included, who provides analysis, and what rights permit storing/showing source text?
4. **Analysis authorship:** Which V1 fields are editorially curated, parser-derived, or user-authored? The proposed default is no automatic interpretation.
5. **Private-data model:** What does “private” mean for Notebook entries and user scripts, and is authentication required for V1?
6. **Evidence granularity:** Are line-based text spans sufficient, or must V1 support page numbers and multiple source formats?
7. **Library navigation:** Is Library a top-level area for saved references, or should Reference Shelf live inside Study and Make?
8. **V1 screenplay editing depth:** Is basic text editing required, or is the Writing Studio initially a preserved source reader with annotations? The current brief requests a working screenplay environment but does not settle editing mechanics.
9. **Transform/Combine Material:** What user-controlled operations and artifact lineage should those names represent? They remain later research items until defined.

## NARRATIVE LAB V1 — PRODUCT MAP

```text
NARRATIVE LAB
├── HOME
├── STUDY
│   ├── Story Atlas
│   └── Work Page
│       ├── Structure / Scene Index
│       ├── Scene Study
│       │   ├── Narrative Anatomy
│       │   ├── Characters → Character Study
│       │   ├── Relationships (basic contextual view)
│       │   ├── Information / Mechanisms (basic contextual views)
│       │   └── Evidence (FACT / INFERENCE / INTERPRETATION)
│       └── Reference actions
├── MAKE
│   ├── My Works / Source Intake
│   └── Writing Studio / Screenplay Lab
│       ├── Scene Work / Basic Annotations
│       └── Writer's Notebook
├── LIBRARY
│   └── Reference Shelf
└── COMMON
    ├── Search
    ├── Contextual Navigation
    └── Shared Narrative Model
```

## NARRATIVE LAB LATER — ROADMAP

```text
1. Deepen study
   ├── Guided Study Sessions
   ├── Narrative Knowledge / Mechanism Library
   └── Themes, Motifs, and Conventions Index
2. Trace narrative change
   ├── Character Trajectory
   ├── Relationship Trajectory
   ├── Information Flow and Setup / Payoff Tracing
   ├── Narrative Graph, Scene Relations, and Dependency Tracing
   └── Cross-Work Mechanism Tracing
3. Compare and revise
   ├── Comparison Workspace / Structural Comparison
   ├── Draft History and Comparison
   └── Revision Tools
4. Explore making
   ├── Transformation Workspace (research / experimental)
   └── Combine Material (research / experimental)
5. Extend personal and shared context
   ├── Work / Study History
   └── Discussion / Sharing (optional; only after privacy and collaboration are defined)
```
