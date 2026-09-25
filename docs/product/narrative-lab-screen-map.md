# Narrative Lab V1 Screen Map

## Purpose and basis

This document translates the current [Narrative Lab feature map](narrative-lab-feature-map.md) into navigation, screens, contextual views, and workspace states. The feature map remains the product source of truth; this document defines where its V1 capabilities appear and how users move among them.

This is application architecture documentation only. It does not specify routes, UI components as code, APIs, persistence implementation, or visual designs.

## Top-level product areas

Use four top-level destinations, with Study and Make as the two primary work modes:

| Destination | Role | Default entry |
| --- | --- | --- |
| **Home** | Shared editorial entry and honest continue-work context. | Home screen |
| **Study** | Understand existing Works and their linked narrative objects. | Story Atlas |
| **Make** | Develop the user's own Works. | My Works |
| **Library** | Return to the user's saved references. | Reference Shelf |

**Search** is a global action available from all four areas, not another mode or top-level destination. Characters, relationships, information, mechanisms, anatomy, evidence, and notes are contextual destinations inside a Work or screenplay workspace; they do not become global tabs.

This chooses the four destinations already proposed in the feature map. Study and Make remain modes over the shared narrative model. Home and Library are shared entry/retrieval areas. The exact naming and whether Library merits a top-level destination remain product decisions noted below.

## V1 feature-to-view map

The following entries cover every V1 feature in the feature map. A feature does not automatically get a full screen: contextual features are rendered inside a Work or workspace, and shared foundations have no standalone view.

### V1-01 — Home

- **SCREEN / VIEW:** Full screen — Home.
- **MODE:** Common.
- **PURPOSE:** Editorial entry into featured study, discoveries, and current work.
- **ENTRY POINT:** App launch or Home destination.
- **PRIMARY USER ACTION:** Open the featured study or continue a current Work.
- **SECONDARY ACTIONS:** Browse work discovery; open a recent study only when real history is available; enter Study or Make.
- **DATA REQUIRED:** Curated Work cards; a valid current/recent Work reference if shown.
- **NARRATIVE OBJECTS USED:** Work, Scene, Mechanism, Evidence, user-to-Work references.
- **DESTINATIONS:** Story Atlas, Work Page, Scene Study, My Works/Writing Studio.
- **MOBILE PRESENTATION:** One column; featured study then discovery and current work. No desktop-style cards squeezed side by side.
- **TABLET PRESENTATION:** Featured work with reduced discovery columns; current work remains visible without competing panes.
- **DESKTOP PRESENTATION:** Editorial lead item plus discovery and current-work areas in a wider reading layout.

### V1-02 — Story Atlas

- **SCREEN / VIEW:** Full screen — Study landing/catalog.
- **MODE:** Study.
- **PURPOSE:** Browse and search the curated film/screenplay corpus.
- **ENTRY POINT:** Study destination, Home discovery, or a global Search result.
- **PRIMARY USER ACTION:** Search/filter and open a Work.
- **SECONDARY ACTIONS:** Clear filters; save a Work to Reference Shelf; return to Home.
- **DATA REQUIRED:** Available Works and populated metadata/facets.
- **NARRATIVE OBJECTS USED:** Work, Creator display metadata, Scene/Mechanism metadata when indexed.
- **DESTINATIONS:** Work Page, Search results, Reference Shelf.
- **MOBILE PRESENTATION:** Search first, touch-friendly filter control, stacked Work cards; filters appear in a bottom sheet.
- **TABLET PRESENTATION:** Compact result list with a filter drawer or reduced visible facet row.
- **DESKTOP PRESENTATION:** Search and facets beside a scannable result list; Work detail opens as a full contextual destination.

### V1-03 — Work Page

- **SCREEN / VIEW:** Full screen — shared Work overview, reused in Study and Make context.
- **MODE:** Study or Make, carried as context rather than a different Work identity.
- **PURPOSE:** Summarize one film/screenplay Work and provide entry to its analysis and source.
- **ENTRY POINT:** Story Atlas, Home, Reference Shelf, My Works, or a contextual link.
- **PRIMARY USER ACTION:** Choose a scene or narrative object to inspect.
- **SECONDARY ACTIONS:** Review metadata and story summary; save/unsave a reference; open the Work in Writing Studio when it is user-owned.
- **DATA REQUIRED:** Work metadata, linked source descriptor, scene index, available character/relationship/information/mechanism summaries, and evidence availability.
- **NARRATIVE OBJECTS USED:** Work, Source/Document, World, Scene, Character, Relationship, Event, Structural Unit, Information, Mechanism, Evidence.
- **DESTINATIONS:** Scene Study, Character Study context, Reference Shelf, Writing Studio (user Works only), Search.
- **MOBILE PRESENTATION:** Stacked editorial metadata and sections; scenes and linked objects open sequentially with a persistent contextual back path.
- **TABLET PRESENTATION:** Work summary plus one selected scene/object panel; other sections open in drawers.
- **DESKTOP PRESENTATION:** Work overview with scene index and a selected section/object panel; no permanent tab for every object type.

### V1-04 — Scene Study

- **SCREEN / VIEW:** Full screen — Study workspace, with contextual pane states.
- **MODE:** Study.
- **PURPOSE:** Read a source scene and inspect its structure/anatomy with evidence.
- **ENTRY POINT:** Scene list/index on Work Page, Search result, linked object, or direct return to a prior scene.
- **PRIMARY USER ACTION:** Read the screenplay and inspect scene anatomy.
- **SECONDARY ACTIONS:** Open Character/Relationship/Information/Mechanism details; inspect Evidence; save a Reference; add a private Note if the user's permissions allow.
- **DATA REQUIRED:** Source text and stable scene boundaries; scene metadata; linked characters/objectives/obstacles/information/change/function; evidence spans and claim status.
- **NARRATIVE OBJECTS USED:** Work, Source/Document, Scene, Character, Relationship, Objective, Obstacle, Information, Event, Beat, Narrative State, Mechanism, Evidence, Note/Annotation.
- **DESTINATIONS:** Contextual views listed below; return to Work Page or original search/reference context.
- **MOBILE PRESENTATION:** Sequential states within the same scene context: scene index → screenplay → anatomy → evidence/object detail. Use sheets for short context and full sequential views for longer material.
- **TABLET PRESENTATION:** Screenplay plus one analysis pane; scene index and object/evidence detail open in drawers or split views.
- **DESKTOP PRESENTATION:** Persistent Scene Index, primary Screenplay, and contextual Narrative Anatomy pane. Evidence and linked object detail occupy the contextual pane, not another global screen.

### V1-05 — Character Study

- **SCREEN / VIEW:** Contextual view in the Work/Scene inspector; not a top-level screen.
- **MODE:** Study.
- **PURPOSE:** Inspect a character's appearances, objectives, relationships, information, and supported changes in the current Work.
- **ENTRY POINT:** Character list on Work Page or a Character link from Scene Study.
- **PRIMARY USER ACTION:** Open a relevant scene/evidence item from the character context.
- **SECONDARY ACTIONS:** Return to the originating Scene/Work; open a linked Relationship or Information view.
- **DATA REQUIRED:** Character record and ordered links to scenes, events, objectives, relationships, and evidence.
- **NARRATIVE OBJECTS USED:** Character, Scene, Objective, Relationship, Event, Information, Narrative State, Evidence.
- **DESTINATIONS:** Scene Study, Relationship view, Evidence view, Work Page.
- **MOBILE PRESENTATION:** Sequential Character summary and appearance list; selecting an appearance opens Scene Study with the originating Character retained as return context.
- **TABLET PRESENTATION:** Character details in inspector drawer alongside the selected scene where space allows.
- **DESKTOP PRESENTATION:** Character detail replaces the inspector content while the selected scene/index context stays visible.

### V1-06 — Narrative Anatomy

- **SCREEN / VIEW:** Contextual inspector view/section in Work Page or Scene Study; not a standalone screen.
- **MODE:** Study and Make.
- **PURPOSE:** Show basic sequence, function, objective/obstacle, information, and change relationships without advanced graph navigation.
- **ENTRY POINT:** Work Page structure section or Scene Study's default inspector.
- **PRIMARY USER ACTION:** Select an ordered scene or anatomy item to inspect its linked objects.
- **SECONDARY ACTIONS:** Switch to a linked Character, Relationship, Information, Mechanism, or Evidence view.
- **DATA REQUIRED:** Scene order, structural units when supplied, scene analysis, explicit causal links, and evidence references.
- **NARRATIVE OBJECTS USED:** Work, Structural Unit, Scene, Event, Beat, Objective, Obstacle, Information, Narrative State, Mechanism, Evidence.
- **DESTINATIONS:** Scene Study, Character Study, contextual object views, Evidence view.
- **MOBILE PRESENTATION:** Stacked anatomy sections ordered by scene; select a section for a focused view and return to the same scene.
- **TABLET PRESENTATION:** Inspector section beside the screenplay or in an expandable drawer.
- **DESKTOP PRESENTATION:** Contextual inspector alongside screenplay; Anatomy is the default content, not a fourth persistent pane.

### V1-07 — Evidence and Claim Status

- **SCREEN / VIEW:** Contextual Evidence view rendered in the inspector; tablet drawer; phone bottom sheet or sequential detail.
- **MODE:** Study and Make.
- **PURPOSE:** Let a user trace a claim to source and distinguish FACT, INFERENCE, and INTERPRETATION.
- **ENTRY POINT:** Evidence marker/link from Work Page, Scene Study, Character Study, or an annotation.
- **PRIMARY USER ACTION:** Inspect the source span and claim status.
- **SECONDARY ACTIONS:** Jump to the source location; return to the exact claim/object; attach a source span to a basic Make annotation.
- **DATA REQUIRED:** Source identity, stable location/span, linked claim/observation, status, and optional confidence.
- **NARRATIVE OBJECTS USED:** Evidence, Source/Document, Work, Scene, Beat, Character, Information, Note/Annotation.
- **DESTINATIONS:** Original source/scene, originating anatomy section, linked Character or Information context.
- **MOBILE PRESENTATION:** Bottom sheet for a short evidence excerpt; expand to sequential detail for long spans; close returns to selected claim and scroll position.
- **TABLET PRESENTATION:** Evidence drawer or split view while preserving the selected screenplay span.
- **DESKTOP PRESENTATION:** Evidence content in the right contextual pane; source remains highlighted in the center screenplay pane.

### V1-08 — Search

- **SCREEN / VIEW:** Full screen — global search results; search field also appears as a shared action.
- **MODE:** Common.
- **PURPOSE:** Find available Works and indexed narrative metadata.
- **ENTRY POINT:** Global Search action, Story Atlas search, or supported work-context search.
- **PRIMARY USER ACTION:** Enter a query and open a result.
- **SECONDARY ACTIONS:** Apply/clear supported metadata filters; refine query; return to the originating context.
- **DATA REQUIRED:** Search index over available Work and metadata fields; result context path.
- **NARRATIVE OBJECTS USED:** Work, Character, Scene, Location, Mechanism, Theme/Motif only when V1 data is indexed, Reference.
- **DESTINATIONS:** Work Page, Scene Study, Character Study context, Reference Shelf.
- **MOBILE PRESENTATION:** Full-page query and stacked results; filters open as a bottom sheet.
- **TABLET PRESENTATION:** Search/results page with a reduced facet drawer.
- **DESKTOP PRESENTATION:** Search field, visible scope/facets, and results list; selected result opens its contextual destination.

### V1-09 — Reference Shelf

- **SCREEN / VIEW:** Full screen — Library destination.
- **MODE:** Common, primarily Study.
- **PURPOSE:** Show a user's saved Work, Scene, and Mechanism references, distinct from the curated Story Atlas.
- **ENTRY POINT:** Library destination or save action from a Work/Scene/Mechanism context.
- **PRIMARY USER ACTION:** Open a saved item.
- **SECONDARY ACTIONS:** Remove a saved reference; return to its prior context.
- **DATA REQUIRED:** User-scoped reference links to stable narrative object IDs.
- **NARRATIVE OBJECTS USED:** UserReference, Work, Scene, Mechanism.
- **DESTINATIONS:** Work Page, Scene Study, Mechanism contextual view.
- **MOBILE PRESENTATION:** Stacked saved items with touch-friendly open/remove actions.
- **TABLET PRESENTATION:** List with a detail drawer.
- **DESKTOP PRESENTATION:** Saved-item list with selected-item preview/context.

### V1-10 — My Works

- **SCREEN / VIEW:** Full screen — Make landing/Work list.
- **MODE:** Make.
- **PURPOSE:** List and create the user's screenplay Works.
- **ENTRY POINT:** Make destination or return from Writing Studio.
- **PRIMARY USER ACTION:** Create a Work and provide screenplay source text.
- **SECONDARY ACTIONS:** Reopen an existing Work; inspect source/parse readiness; remove/archive only if that operation is later defined.
- **DATA REQUIRED:** User-owned Work metadata, source descriptor, and parse state.
- **NARRATIVE OBJECTS USED:** Work, Source/Document, Scene, ScriptBlock.
- **DESTINATIONS:** Work Page, Writing Studio.
- **MOBILE PRESENTATION:** Stacked Work list and simplified intake form; show explicit parse/save state.
- **TABLET PRESENTATION:** List with source-intake sheet or split detail.
- **DESKTOP PRESENTATION:** Work list and selected source/status details; intake does not replace the list context unnecessarily.

### V1-11 — Writing Studio / Screenplay Lab

- **SCREEN / VIEW:** Full screen — Make workspace. Scene reading/editing uses the shared workspace shell.
- **MODE:** Make.
- **PURPOSE:** Keep the user's screenplay primary while exposing scene navigation, anatomy, and notes.
- **ENTRY POINT:** My Works or Work Page's “Open in Writing Studio” action for an owned Work.
- **PRIMARY USER ACTION:** Select a scene and work with its screenplay context.
- **SECONDARY ACTIONS:** Open anatomy, view/add annotations, save the current note/annotation, jump to evidence, return to Work.
- **DATA REQUIRED:** Original screenplay/source, scene mapping, current user annotations/notes, linked narrative analysis.
- **NARRATIVE OBJECTS USED:** Work, Source/Document, Scene, Character, Beat, Objective, Obstacle, Evidence, Note/Annotation.
- **DESTINATIONS:** Scene Work, Scene Study context, Notebook, Work Page.
- **MOBILE PRESENTATION:** Sequential scene index → screenplay → anatomy/notes; retain Work and Scene context in the header/back path.
- **TABLET PRESENTATION:** Screenplay plus one analysis/notes pane; scene list or secondary pane in drawer.
- **DESKTOP PRESENTATION:** Scene Index + primary Screenplay + contextual inspector. Editing depth is unresolved; the screen map does not assume a full screenplay editor.

### V1-12 — Scene Work and Basic Annotations

- **SCREEN / VIEW:** Contextual view in Writing Studio; annotation editor is a drawer/sheet, not a separate screen.
- **MODE:** Make.
- **PURPOSE:** Attach a private note or basic tag to a Scene or stable selected source span.
- **ENTRY POINT:** Scene action or text selection in Writing Studio.
- **PRIMARY USER ACTION:** Add/edit an annotation and explicitly save it.
- **SECONDARY ACTIONS:** Change annotation type; jump to the source span; close and return to the selection.
- **DATA REQUIRED:** Work/Scene, source span, annotation kind, note text, save state.
- **NARRATIVE OBJECTS USED:** Scene, Beat, Objective, Obstacle, Information, Source/Document, Note/Annotation, optional Evidence.
- **DESTINATIONS:** Same screenplay selection, Narrative Anatomy, Notebook if user explicitly copies/links material.
- **MOBILE PRESENTATION:** Bottom-sheet editor over the selected screenplay passage; save returns to the same passage.
- **TABLET PRESENTATION:** Drawer/sheet with selection context visible in the screenplay split view.
- **DESKTOP PRESENTATION:** Inspector editor adjacent to screenplay; annotation marker anchors to the selected passage.

### V1-13 — Writer's Notebook

- **SCREEN / VIEW:** Full screen — private Notebook list/editor; a new-entry editor may be an inline state.
- **MODE:** Make.
- **PURPOSE:** Store private observations, ideas, fragments, questions, and research notes.
- **ENTRY POINT:** Make area, Home entry point, or contextual “Add to Notebook” action.
- **PRIMARY USER ACTION:** Create/edit a private text note and save it.
- **SECONDARY ACTIONS:** Search/filter notes; optionally link/unlink a Work, Scene, Character, or Reference.
- **DATA REQUIRED:** User-owned note text, created/updated time, optional tags and object links.
- **NARRATIVE OBJECTS USED:** Note/Material, Work, Scene, Character, Reference.
- **DESTINATIONS:** Linked Work/Scene/Character contexts; return to originating context when opened contextually.
- **MOBILE PRESENTATION:** Note list and editor as sequential views; contextual links open in sheets or linked views.
- **TABLET PRESENTATION:** Split note list/editor or editor sheet.
- **DESKTOP PRESENTATION:** Note list and editor/context pane.

### V1-14 — Shared Narrative Model

- **SCREEN / VIEW:** No standalone screen; shared product/data foundation.
- **MODE:** Study and Make.
- **PURPOSE:** Ensure the same Work/Scene/Character/Evidence identities appear in both modes.
- **ENTRY POINT:** Used by all Work and workspace views; not directly opened by a user.
- **PRIMARY USER ACTION:** Not applicable as a separate action; users navigate linked objects.
- **SECONDARY ACTIONS:** None as a separate screen.
- **DATA REQUIRED:** Canonical object IDs, typed links, source/provenance, ownership/visibility, and claim status.
- **NARRATIVE OBJECTS USED:** All shared narrative objects, plus Source/Document and Note/Material.
- **DESTINATIONS:** Exposed through Work Page, Scene Study, Character Study, Writing Studio, Search, and Reference Shelf.
- **MOBILE PRESENTATION:** Same objects, links, and permissions; sequential views only.
- **TABLET PRESENTATION:** Same objects, links, and permissions; fewer concurrent panes.
- **DESKTOP PRESENTATION:** Same objects, links, and permissions; multi-pane inspection.

### V1-15 — Contextual Navigation and Responsive Workspace

- **SCREEN / VIEW:** Shared application shell and workspace behavior; no separate destination.
- **MODE:** Common to Study and Make.
- **PURPOSE:** Preserve hierarchy and return context while moving among narrative objects.
- **ENTRY POINT:** All top-level destinations and contextual links.
- **PRIMARY USER ACTION:** Open a related object and return to its origin.
- **SECONDARY ACTIONS:** Change mode/destination; close an inspector/drawer; use Work/Scene breadcrumbs.
- **DATA REQUIRED:** Current mode, selected Work/object/source, and contextual navigation stack.
- **NARRATIVE OBJECTS USED:** All linked objects; navigation state is not a narrative record.
- **DESTINATIONS:** Home, Study, Make, Library, Search, and parent Work/Scene/object context.
- **MOBILE PRESENTATION:** Sequential navigation and stacked sections; contextual detail in sheets; visible back/return path.
- **TABLET PRESENTATION:** Reduced panes, drawers, sheets, and split views.
- **DESKTOP PRESENTATION:** Top-level area navigation, Work/Scene context header, and multi-pane workspace where appropriate.

## Core Study workflow

Transition labels: **Full navigation** changes the primary page while retaining a return context. **Pane change** changes the selected content in the current workspace without losing the screenplay. **Drawer/sheet** presents temporary supporting detail and returns to the exact selection that opened it.

| Step | User movement | Transition type | Context retained / return behavior |
| --- | --- | --- | --- |
| 1 | Home → Story Atlas | Full navigation | Home remains a back/breadcrumb parent. |
| 2 | Story Atlas → Work | Full navigation | Atlas query/filter context is retained when returning. |
| 3 | Work → Scene | Full navigation into Scene Study | Work and selected Scene are in the context header; Back returns to the Work Page at its scene section. |
| 4 | Scene → Screenplay | Pane change / focus state | The selected Scene is unchanged; on desktop the screenplay is already the center pane. |
| 5 | Screenplay → Narrative Anatomy | Pane selection within the inspector; phone uses a sequential view | Keep the scene and screenplay position; Anatomy becomes the selected contextual content. |
| 6 | Narrative Anatomy → Evidence | Drawer/sheet or inspector content state | Highlight/retain the supporting source span and claim; close returns to the same anatomy claim. |
| 7 | Evidence → Character / Relationship / Information | Contextual view in the inspector; use a drawer/sheet for a quick detail | Preserve the originating claim, evidence item, Scene, and Work as a return chain. Selecting an appearance may open Scene Study with this object as the return context. |
| 8 | Any contextual view → originating context | Close/Back within context, then full navigation if changing page | Close object detail → Evidence/Anatomy; Back to Scene; Work breadcrumb; Atlas breadcrumb. Do not send the user to a generic root. |

Mechanism detail follows the same contextual pattern as Character/Relationship/Information. It is a basic linked V1 object view, not the later cross-work Mechanism Library.

## Core Make workflow

| Step | User movement | Transition type | Context retained / return behavior |
| --- | --- | --- | --- |
| 1 | Make → My Works | Full navigation to Make's default page | Make remains selected in top-level navigation. |
| 2 | My Works → Work | Full navigation to the shared Work Page | The Work is marked as user-owned; return goes to My Works. |
| 3 | Work → Writing Studio | Full navigation to the shared Make workspace | Keep the Work identity; return to the same Work Page section. |
| 4 | Writing Studio → Scene | Pane/selection change | Set active Scene in the index and header; screenplay remains primary. |
| 5 | Scene → Screenplay | Pane focus/state; no new screen | Preserve selected Scene and text position. |
| 6 | Screenplay → Notes/Annotations | Contextual inspector view or drawer/sheet | Keep selected passage visible/marked; close returns to the same passage. |
| 7 | Notes/Annotations → Save | Save action/state, not navigation | Persist the note/annotation, show saved state, stay with the same Scene/selection. The product map does not define saving edited screenplay versions. |
| 8 | Save → Work | Full navigation via Work breadcrumb or Back | Return to the same Work Page and preserve the Writing Studio return path. |

No AI drafting, advanced revision, draft comparison, or transformation controls appear in this V1 flow.

## Central desktop analytical workspace

The Scene Study and Writing Studio use one workspace shell with mode-specific contextual content:

```text
┌──────────────────────────────────────────────────────────────────┐
│ Work / mode / source / scene context and return path             │
├────────────────┬──────────────────────────┬────────────────────┤
│ SCENE INDEX    │ SCREENPLAY               │ CONTEXT INSPECTOR  │
│ ordered scenes │ primary reading surface  │ Anatomy by default │
│                │ stable source locations  │ Evidence / Objects │
│                │ selected span highlight  │ Notes in Make      │
└────────────────┴──────────────────────────┴────────────────────┘
```

- **Persistent panes:** Scene Index, primary Screenplay, and one contextual inspector. The screenplay receives the largest share of the workspace; the index and inspector remain secondary.
- **Narrative Anatomy:** default inspector content for Scene Study. It shows scene metadata, characters, objective, obstacle, information, change, narrative function, and links to evidence.
- **Characters and Relationships:** links/sections within anatomy. Selecting one replaces the inspector's content with its contextual detail; it does not add permanent character/relationship columns.
- **Information and Mechanisms:** similarly open as contextual inspector content. V1 shows only available, linked information/mechanism records; broad tracing remains later.
- **Evidence:** opens in the inspector with the source span highlighted in the center pane. Evidence is not a permanently visible fourth pane.
- **Notes/Annotations:** Make-only inspector content or annotation editor attached to a selected span. The original screenplay remains distinct from note text.
- **Selection behavior:** every pane change carries Work ID, Scene ID, source position, and origin context. Opening a related object does not discard the current source selection.
- **Sizing:** use relative space rather than fixed pixel commitments; keep the screenplay wider than either side pane. Exact proportions can be set during design, not in this architecture document.

### Three shared workspace states

These are logical pane configurations, not extra screens:

1. **Study / Scene:** Scene Index | Screenplay | Narrative Anatomy.
2. **Study / Evidence focus:** Scene Index | Screenplay with evidence span | Evidence inspector.
3. **Make / Writing:** Scene Index | Screenplay | Notes/Annotations inspector.

Character, Relationship, Information, and Mechanism details change the inspector's selected content inside these states; they do not create additional workspace states.

## Tablet and phone workspace

### Tablet

- Start with Screenplay plus one secondary pane; do not show all columns at desktop width.
- Scene Index opens as a drawer or occupies a compact split pane.
- Anatomy, linked-object detail, Evidence, and Notes use one inspector drawer/sheet at a time.
- Keep a visible Work/Scene context and a clear close/back action so closing a drawer restores the exact selected text and scene.
- Comparison between two narrative items is not a V1 workspace requirement.

### Phone

- Use a sequential Scene Study flow: Scene Index → Screenplay → Anatomy → Evidence or related object.
- In Writing Studio use: My Works → Work → Scene Index → Screenplay → Notes/Annotations.
- Long screenplay text gets the full reading width; do not permanently share it with side columns.
- Short evidence/object previews use bottom sheets; longer Character/Relationship/Information detail becomes a sequential contextual view.
- Close/Back returns to the originating Work, Scene, selected passage, or claim. Contextual breadcrumbs remain visible.
- Use stacked Work Page sections, explicit section labels, and touch-sized controls. No object type becomes a global phone tab.

## Contextual object navigation rules

```text
WORK
└── SCENE
    ├── SCREENPLAY / SOURCE SPAN
    ├── CHARACTER
    │   └── related SCENES / RELATIONSHIPS / EVIDENCE
    ├── RELATIONSHIP
    │   └── participants / related SCENES / EVIDENCE
    ├── INFORMATION
    │   └── source / appearance in SCENES / EVIDENCE
    ├── MECHANISM
    │   └── scene occurrence / EVIDENCE
    └── NARRATIVE ANATOMY
        └── CLAIM → EVIDENCE → SOURCE SPAN
```

Navigation rules:

- Every contextual object view carries the originating Work and Scene (when applicable).
- A detail view has a local return to its origin. Global Home/Study/Make/Library navigation is not used as a substitute for Back.
- Search results open the relevant context and preserve the query/results location on return.
- Reference Shelf opens the saved object but offers a path back to the Shelf.
- A Character reached from a Scene returns to that Scene; a Character reached from Work Page returns to its Work section.
- Evidence opens at the linked source location and returns to the precise claim that opened it.
- V1 does not expose Mechanism, Relationship, Information, Theme, or Evidence as permanent global navigation tabs.

## Shared UI structures to define (not implement here)

| Shared structure | Use |
| --- | --- |
| Product/mode header | Home, Study, Make, Library, global Search entry, active Work context. |
| Context header and breadcrumbs | Work/Scene/source identity plus meaningful return path. |
| Editorial header | Work/Scene title, creator display text, year/medium/source metadata. |
| Section label and divider | Hierarchy in Work Page, Anatomy, and Notebook without excessive card chrome. |
| Work card | Atlas discovery, Home feature, Search results, Reference Shelf. |
| Scene index row/list | Ordered scene navigation and active-scene context. |
| Screenplay block | Preserve source order/line positioning and distinguish scene heading, action, character cue, dialogue, parenthetical, and transition. |
| Source-span/annotation marker | Link selected text to a note or analytical claim without modifying source text. |
| Narrative Anatomy section | Label objective, obstacle, information, change, function, and related objects. |
| Evidence block | Claim type, source span/location, observation, confidence if present, and return link. |
| Contextual inspector | Anatomy/object/Evidence/Notes content beside the primary screenplay. |
| Drawer/sheet shell | Filters, linked-object quick views, Evidence detail, annotation editor on constrained widths. |
| Search field and filter control | Shared query behavior with explicit supported facets and applied state. |
| Notebook entry/editor | Private note text, timestamps, optional tags and linked objects. |
| Reference item/save action | Saved object summary, type, source context, remove/open action. |
| Save state | Explicit saved/unsaved feedback for annotations/notes; no false confirmation before persistence. |
| Navigation transition | Directional context change with reduced-motion behavior; not a substitute for URL/history decisions. |
| Empty / unavailable / parsing states | Distinguish no data, not yet analyzed, unsupported source, and actual error. |

## Ambiguities to decide before implementation

The screen map chooses where a concept appears without pretending unresolved data/product decisions are settled.

| Concept | Screen-map treatment | Decision still required |
| --- | --- | --- |
| Creator vs `Work.creator` | Show creator names as Work metadata in headers/cards; no Creator screen or canonical Creator route in V1. | Decide whether Creator is a canonical entity or display-only strings, and whether creator search is name matching or entity navigation. Existing Work schema uses `creator: list[str]`; the feature map also names Creator. |
| Work vs film vs screenplay | Work Page is the visible narrative context; screenplay is a source/document displayed inside it. | Decide whether a film and screenplay are one Work with multiple Sources or separate linked Works. Do not collapse their identities in storage/UI. |
| Reference Shelf | Separate Library destination for user-saved object references; distinct from curated Story Atlas. | Confirm top-level Library and define reference scope, grouping, and persistence. |
| Notebook vs Material vs Scene annotation | Notebook is private freeform material; annotation is anchored to a Scene/source span. | Decide whether they share one Note model with types or are separate entities, and whether notes can be copied/linked without duplication. |
| Mechanism | A V1 contextual object detail reachable from Work/Scene; no global Mechanism Library screen. | Define mechanism taxonomy, who assigns it, and how a proposed pattern differs from a supported claim. |
| Evidence | Contextual inspector/sheet that highlights a source span and returns to its claim. | Define stable source offsets across formats and add claim status; current Evidence model lacks FACT/INFERENCE/INTERPRETATION. |
| Analysis vs interpretation | Work/Scene/Character views display labeled claims; INTERPRETATION is never presented as source fact. | Decide whether Analysis is an entity or a collection of typed claims, and who authors/reviews each claim. |
| Recent/current work vs Study History | Home shows current/recent items only when stored; no V1 History screen. | Define how “current” is chosen and what events qualify for later Study History. |
| Save behavior | V1 Save applies to notes/annotations and remains in the same context; screen map does not define screenplay version saving. | Decide explicit save vs autosave, draft recovery, and whether V1 Writing Studio edits source text or initially reads source plus annotations. |
| Scene/source identity | Scene Study and Writing Studio use stable scene IDs and source positions. | Decide how scene boundaries survive parser changes and whether annotations attach to the source version or logical Scene across versions. |
| Work ownership/privacy | My Works, Notebook, Reference Shelf are user-scoped views. | Decide account requirement, local-only vs synced storage, sharing defaults, and deletion/export behavior. |
| Search scope | Global Search is one screen/action with context-preserving results. | Decide exactly which fields and narrative objects are indexed in V1; advanced semantic search is out of scope. |
| Home / Study / Make / Library labels | Use four destinations as proposed by the feature map. | Validate whether Library is top-level or a section under Study/Make before implementation. |

## NARRATIVE LAB V1 SCREEN MAP

### Exact view counts

These counts refer to unique logical V1 view definitions, not breakpoints or duplicate routes. A contextual view may render in a pane, drawer, or sheet depending on device; it is counted once in its primary category.

- **Full screens: 9** — Home; Story Atlas; Work Page; Scene Study; Search; Reference Shelf; My Works; Writing Studio; Writer's Notebook.
- **Contextual views: 8** — Screenplay/source reader; Narrative Anatomy; Character Study; Relationship detail; Information detail; Mechanism detail; Evidence detail; Scene Work/Notes/Annotations.
- **Drawers/sheets: 4** — Atlas filter drawer; related-object quick view; Evidence detail on constrained widths; annotation editor on constrained widths.
- **Shared workspace states: 3** — Study/Scene; Study/Evidence focus; Make/Writing.

Drawers/sheets are presentation forms of the contextual views, so the category totals should not be added together as if they were independent screens. Shared narrative model and navigation shell are foundations and do not add screens.

### Concise navigation tree

```text
NARRATIVE LAB
├── HOME
├── STUDY
│   └── STORY ATLAS
│       └── WORK PAGE
│           └── SCENE STUDY
│               ├── Scene Index
│               ├── Screenplay / Source
│               ├── Narrative Anatomy
│               ├── Character Study
│               ├── Relationship detail
│               ├── Information / Mechanism detail
│               └── Evidence → source span → return to claim
├── MAKE
│   ├── MY WORKS
│   │   └── WORK PAGE
│   │       └── WRITING STUDIO
│   │           └── Scene Work
│   │               ├── Screenplay / Source
│   │               └── Notes / Annotations → Save → return to selection
│   └── WRITER'S NOTEBOOK (private; also reachable contextually from Work/Scene)
├── LIBRARY
│   └── REFERENCE SHELF
├── COMMON
│   └── SEARCH (global action; full results screen)
```
