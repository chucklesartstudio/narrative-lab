# Studio Feature Inventory and Narrative Lab Mapping

## Scope and evidence

This is a source-led inventory of the Studio prototype in `project-bolt-sb1-tmoqsywr.zip`. It cross-checks the screens, app state, handlers, and data modules rather than treating screen copy or the earlier Studio design brief as proof that a feature works. The earlier design-system extraction is in [studio-derived-system.md](studio-derived-system.md).

The attached second-pass request defines the analysis and document requested here. The Studio archive's `.bolt/prompt` is generic Bolt project guidance; it is not treated as product behavior or as a separate request. Status labels below describe the code in the archive.

### Status labels

- **IMPLEMENTED** — an interaction or presentation behavior exists and runs in the prototype, generally in local UI state.
- **PARTIALLY IMPLEMENTED** — a useful part exists, but the larger workflow or a key behavior is incomplete.
- **VISUAL PLACEHOLDER** — the screen or control is drawn, but its central device or task behavior is not implemented.
- **STATIC DATA** — the screen's primary content is hard-coded example data, not user-generated or persisted records.
- **SPECIFICATION ONLY** — a requested/mentioned capability has no corresponding Studio implementation in the supplied source.

A feature may have one primary status plus an explicit static-data note. `SPECIFICATION ONLY` rows are included because the inventory request named them; they are not counted as present Studio features.

### Source/runtime facts

- **Client:** Vite 5, React 18, TypeScript 5, Tailwind CSS 3, and Lucide React. The screen flow is a local React app, not URL-based routing.
- **State/data:** local `useState` and static TypeScript data modules. There are no `fetch`, browser-storage, camera, microphone, or `MediaRecorder` calls in `src/`.
- **Supabase:** `@supabase/supabase-js` appears in `package.json`, but no source file imports it or uses a client.
- **Assets:** the prototype uses bundled image files and some remote image URLs. `src/utils/image.ts` appends image-size query parameters to remote URLs.
- **Global UI:** `App.tsx`, `BottomNav.tsx`, `Logo.tsx`, and `ScreenTransition.tsx` compose the screen shell, local screen history, brand mark, and transitions.

## Feature inventory

There are 30 inventory records below. Records 24–27 call out checklist items that are absent or only represented visually, so the count does not imply 30 working product features.

### Entry, home, and navigation

#### 01. Splash / entry experience

- **Studio screen / source:** Splash; `project/src/screens/Splash.tsx`, `project/src/components/Logo.tsx`, `project/src/App.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Underlying pattern:** immersive, staged first entry.
- **User → system:** Continue opens onboarding; Explore as Guest sets the local user type to `prospective` and opens Home.
- **Inputs → outputs:** button choice → next local screen; no credentials or account data.
- **State / navigation / persistence:** a timed `visible` state stages the reveal; navigation is pushed through the app's local history. Nothing is saved across reloads.
- **UI / interaction:** full-viewport image, dark gradient, editorial title, delayed CTA reveals. Image is a bundled sample still.
- **Dependencies:** App screen callbacks, `Logo`, CSS motion, bundled image. No authentication service.

#### 02. Onboarding / context selection

- **Studio screen / source:** Onboarding; `project/src/screens/Onboarding.tsx`, `project/src/App.tsx`, `project/src/types.ts`.
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Underlying pattern:** lightweight first-run context selection.
- **User → system:** select Enrolled Student, Prospective Student, or Alumni / Working Actor, then Enter the Studio; no selection defaults to Enrolled Student.
- **Inputs → outputs:** selected `UserType` → local `userType` and Home screen.
- **State / navigation / persistence:** the selected value exists in component/app memory only. It does not change access, stored settings, or Home content beyond the local state read.
- **UI / interaction:** selectable cards with a radio-like indicator and a CTA whose appearance changes with selection.
- **Dependencies:** App callback and `UserType`. No account, school, teacher, or onboarding API.

#### 03. Home / curated front page

- **Studio screen / source:** Home; `project/src/screens/Home.tsx`, `project/src/App.tsx`, `project/src/data/atlas.ts`, `project/src/data/practice.ts`.
- **Status:** **PARTIALLY IMPLEMENTED**; content is static.
- **Underlying pattern:** curated editorial home with return-to-work and discovery entry points.
- **User → system:** open the featured Atlas item, browse the Atlas row, open today's practice, or open the journal.
- **Inputs → outputs:** hard-coded featured entry, Atlas records, current practice, and a constant streak value → navigation callbacks and displayed summary cards.
- **State / navigation / persistence:** a timed header reveal is transient. `practiceStreak` is initialized to `14` in `App.tsx`; the current-week and Atlas data come from local modules. No user-specific home state is persisted.
- **UI / interaction:** large image-led feature with gradients; horizontal Atlas cards; rehearsal summary; journal card; streak shown only for enrolled users.
- **Dependencies:** Atlas and practice static data, `imgSrc`, App callbacks, bottom navigation.

#### 04. Bottom navigation

- **Studio screen / source:** shared shell; `project/src/components/BottomNav.tsx`, `project/src/App.tsx`, `project/src/types.ts`.
- **Status:** **IMPLEMENTED** in the prototype.
- **Underlying pattern:** persistent top-level destination switcher with active-state feedback.
- **User → system:** choose Home, Practice, Library, Community, or Profile; the app switches to that tab's root.
- **Inputs → outputs:** `NavTab` click → `NAV_TAB_SCREENS` destination and cleared local history.
- **State / navigation / persistence:** active tab is derived from the current screen; tab changes clear the in-memory back stack. The bar is hidden on splash, onboarding, Atlas detail, Daily Practice, and session completion.
- **UI / interaction:** fixed five-item bar, custom SVG icons, active marker, and an elevated center Practice control.
- **Dependencies:** App tab mapping. The 430px cap and five-actor-product tabs are not a responsive navigation solution for Narrative Lab.

#### 05. Contextual screen history and back navigation

- **Studio screen / source:** shared shell; `project/src/App.tsx`, `project/src/types.ts`, back controls in screen files.
- **Status:** **IMPLEMENTED** in memory.
- **Underlying pattern:** contextual navigation with a return path.
- **User → system:** open a nested screen and use its back control to return to the prior screen; switching tabs starts a new tab root.
- **Inputs → outputs:** screen callback → `history` stack and current `screen`.
- **State / navigation / persistence:** history is a React state array. If empty, `goBack` falls back to Home. It is neither URL-addressable nor persisted; browser Back is not wired to this stack.
- **UI / interaction:** detail headers name the return context (for example, Atlas or Library).
- **Dependencies:** `App.tsx` callbacks and each screen's `onBack` prop.

#### 06. Screen transitions

- **Studio screen / source:** shared shell; `project/src/components/ScreenTransition.tsx`, `project/src/App.tsx`, `project/src/index.css`.
- **Status:** **IMPLEMENTED** in the prototype.
- **Underlying pattern:** directional, transition-aware navigation.
- **User → system:** navigation direction passed by the caller selects push, pop, or fade entry.
- **Inputs → outputs:** `screenKey` and direction → opacity and horizontal transform changes.
- **State / navigation / persistence:** transient entry phase, keyed by the local transition counter; no persistence.
- **UI / interaction:** about 300ms opacity/position transition; screens also use staggered fades and slight upward movement; the hero may drift slowly.
- **Dependencies:** React effects, `requestAnimationFrame`, CSS. No reduced-motion behavior is defined in the source.

### Practice and library

#### 07. Daily Practice / guided session

- **Studio screen / source:** Daily Practice; `project/src/screens/DailyPractice.tsx`, `project/src/data/practice.ts`, `project/src/App.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**; session content and progress context are static.
- **Underlying pattern:** guided, sequential session with gated steps.
- **User → system:** open an available exercise, complete it, then continue to the next uncompleted exercise; completing all five opens Session Complete.
- **Inputs → outputs:** clicks against the five static exercise records → in-memory completed set, progress bar, next exercise, and completion transition.
- **State / navigation / persistence:** `completed` is a local `Set`; later steps are gated by the previous step. State resets on remount/reload. The session is not recorded to a user history.
- **UI / interaction:** numbered progress, cards show type/duration/objective, disabled upcoming items, completion check, delayed auto-advance.
- **Dependencies:** `currentWeek` data, `App.tsx` completion callback. No session service or persistence.

#### 08. Exercise detail within Daily Practice

- **Studio screen / source:** nested Exercise Detail; `project/src/screens/DailyPractice.tsx`, `project/src/data/practice.ts`.
- **Status:** **IMPLEMENTED** as part of the local practice flow.
- **Underlying pattern:** focused instruction/detail view with a primary completion action.
- **User → system:** read the exercise objective and instructions, then mark it done; the view advances to the next available exercise or returns to the list.
- **Inputs → outputs:** static exercise record and completion click → updated parent local `Set` and next view.
- **State / navigation / persistence:** completion is held by Daily Practice and disappears when its state resets.
- **UI / interaction:** type/duration badge, editorial title, teacher byline, ordered instructions, fixed bottom CTA.
- **Dependencies:** Daily Practice state and static practice data; teacher data is text, not a teacher workflow.

#### 09. Session completion

- **Studio screen / source:** Session Complete; `project/src/screens/SessionComplete.tsx`, `project/src/App.tsx`.
- **Status:** **IMPLEMENTED** as a local presentation state.
- **Underlying pattern:** clear end state with a next action.
- **User → system:** choose Log a reflection or Return to Home. Log a reflection opens Observation Journal.
- **Inputs → outputs:** completion flag and button → journal or Home screen.
- **State / navigation / persistence:** `showComplete` is local. The journal receives no session ID or reflection context, and completion does not update a lasting record.
- **UI / interaction:** staged reveal, summary text, two CTAs; no XP, badges, or confetti.
- **Dependencies:** Daily Practice completion callback and App navigation.

#### 10. Practice Library

- **Studio screen / source:** Library tab; `project/src/screens/PracticeLibrary.tsx`, `project/src/data/craft.ts`, `project/src/App.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**; listings use static data and several destinations are placeholders.
- **Underlying pattern:** browseable collection of tools and structured learning material.
- **User → system:** open Atlas, Script Lab, Self-Tape Studio, Voice Studio, or a craft category.
- **Inputs → outputs:** selected card/category → local screen transition.
- **State / navigation / persistence:** no saved filters or recent state; content comes from hard-coded arrays.
- **UI / interaction:** compact two-column tool cards followed by ruled category rows with descriptions and counts.
- **Dependencies:** App callbacks and `craftCategories`. Cards leading to placeholder screens do not make those tools functional.

#### 11. Craft Category browsing

- **Studio screen / source:** Craft Category; `project/src/screens/CraftCategory.tsx`, `project/src/data/craft.ts`.
- **Status:** **PARTIALLY IMPLEMENTED**; category contents are static.
- **Underlying pattern:** topic page with type-based subnavigation.
- **User → system:** choose Exercises, Courses, Demonstrations, Reading, or Audio; view matching category items; open an item only when it is an exercise with exercise data.
- **Inputs → outputs:** active tab and category static data → filtered list or an Exercise Viewer.
- **State / navigation / persistence:** `activeTab` and `openExercise` are local; returning from the viewer retains the category's current tab while mounted.
- **UI / interaction:** category description, horizontally scrollable tabs, muted empty-type tabs, item cards and type icons.
- **Dependencies:** `craftCategories` and nested Exercise Viewer. Non-exercise types are displayed but do not open a detail workflow.

#### 12. Exercise Viewer from Craft Category

- **Studio screen / source:** nested Exercise Viewer; `project/src/screens/CraftCategory.tsx`, `project/src/data/craft.ts`.
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Underlying pattern:** single-item guided content with a completion acknowledgment.
- **User → system:** read a static exercise and click Mark Complete; the button changes to Marked Complete and back returns to the category.
- **Inputs → outputs:** exercise data and click → local `done` flag.
- **State / navigation / persistence:** `done` belongs to the viewer instance, resets when it is closed/reopened, and is not written back to the category or profile.
- **UI / interaction:** objective, ordered steps, type/time badge, fixed completion CTA.
- **Dependencies:** exercise item in `craftCategories`; no completion store.

### Atlas and analytical content

#### 13. Performance Atlas

- **Studio screen / source:** Performance Atlas; `project/src/screens/PerformanceAtlas.tsx`, `project/src/data/atlas.ts`, `project/src/App.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**; entries are static.
- **Underlying pattern:** curated analytical archive with browse, search, and detail navigation.
- **User → system:** search/filter the list and open an entry.
- **Inputs → outputs:** query and Atlas array → displayed entry list; selected entry ID → Atlas Entry.
- **State / navigation / persistence:** query and selected-chip state are local and reset when leaving the screen. No saved searches or backend index.
- **UI / interaction:** sticky search/filter header, count, thumbnailed rows, one-line curatorial summary.
- **Dependencies:** `atlasEntries`, `imgSrc`, App open-entry/back callbacks.

#### 14. Atlas text search

- **Studio screen / source:** search control in Performance Atlas; `project/src/screens/PerformanceAtlas.tsx`.
- **Status:** **IMPLEMENTED** for immediate client-side filtering.
- **Underlying pattern:** deterministic metadata search.
- **User → system:** type a query; the list filters as text changes.
- **Inputs → outputs:** lowercased text → entries matching actor, film, director, or any tag.
- **State / navigation / persistence:** local `query`; cleared on screen remount. It does not search year or full analysis text.
- **UI / interaction:** search icon, placeholder names fields, result count updates with the list.
- **Dependencies:** static `atlasEntries`; no network or semantic search.

#### 15. Atlas filter chips

- **Studio screen / source:** filter controls in Performance Atlas; `project/src/screens/PerformanceAtlas.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Underlying pattern:** metadata facets that narrow an archive.
- **User → system:** click All, Actor, Film, Director, or Method Tradition; the selected appearance changes.
- **Inputs → outputs:** selected label → visual active state only. The `filtered` calculation does not use `activeFilter`, so result records do not change.
- **State / navigation / persistence:** `activeFilter` is local presentation state and is reset on remount.
- **UI / interaction:** horizontally scrollable pills with active copper fill.
- **Dependencies:** local React state. No facet metadata mapping is applied.

#### 16. Atlas Entry / editorial detail

- **Studio screen / source:** Atlas Entry; `project/src/screens/AtlasEntry.tsx`, `project/src/data/atlas.ts`.
- **Status:** **PARTIALLY IMPLEMENTED**; some entries display a development placeholder instead of analysis.
- **Underlying pattern:** contextual detail page with introductory context followed by sequenced analysis.
- **User → system:** read the entry and use the floating Atlas back control; scrolling changes the header treatment.
- **Inputs → outputs:** selected static entry → hero, metadata, curatorial text, analysis sections, image credit, and reflection questions.
- **State / navigation / persistence:** local scroll-derived `scrolled`; entry selection is held by App. No annotations, bookmarks, or personal notes persist.
- **UI / interaction:** image-led header; long-form labeled sections for synopsis, context, scene analysis, objective, obstacle, subtext, physical choices, voice, silence, camera, explanation, exercise, and questions; sticky contextual header after scrolling.
- **Dependencies:** `atlasEntries` and `imgSrc`. The page does not carry source spans or evidence IDs for its claims.

### Screenplay, recording, and personal material

#### 17. Script Lab

- **Studio screen / source:** Script Lab; `project/src/screens/ScriptLab.tsx`, `project/src/App.tsx`.
- **Status:** **VISUAL PLACEHOLDER**.
- **Underlying pattern:** intended annotated-text workspace, inferred from screen name and copy.
- **User → system:** the screen presents an upload control and two demonstration-scene cards, but none has a click handler. Only the back button works.
- **Inputs → outputs:** no script input is accepted; no parsed script, opened scene, or annotation output is produced.
- **State / navigation / persistence:** no screen-local state or saved work.
- **UI / interaction:** dashed upload card, PDF/Final Draft/plain-text copy, demo-scene cards, and a message claiming tags/comments are available after opening a scene; no such scene-open state exists in this source.
- **Dependencies:** App back callback only. No file input, parser, editor, selection, annotation, or comment model.

#### 18. Self-Tape Studio

- **Studio screen / source:** Self-Tape Studio; `project/src/screens/SelfTapeStudio.tsx`, `project/src/App.tsx`.
- **Status:** **VISUAL PLACEHOLDER**; recent-take content is static data.
- **Underlying pattern:** media recording and take-history workflow, as described by labels.
- **User → system:** camera workspace and Begin Session are shown, but Begin Session has no handler. Only back navigation works.
- **Inputs → outputs:** no camera stream or recording input; no video output.
- **State / navigation / persistence:** no recording, take, upload, review, or submission state. Three recent takes are hard-coded.
- **UI / interaction:** 16:9 camera placeholder and Recent Takes list with dates/duration/status.
- **Dependencies:** icons and static JSX only. No browser camera API or media recorder.

#### 19. Voice Studio

- **Studio screen / source:** Voice Studio; `project/src/screens/VoiceStudio.tsx`, `project/src/App.tsx`.
- **Status:** **VISUAL PLACEHOLDER**; drill/session descriptions are static data.
- **Underlying pattern:** guided audio practice and recording comparison, based on the displayed copy.
- **User → system:** play controls and drills are shown but have no handlers; only back navigation works.
- **Inputs → outputs:** no microphone/audio input and no playback or comparison output.
- **State / navigation / persistence:** no active session or saved recording state.
- **UI / interaction:** today's session card, play button, microphone copy, color-coded drill rows.
- **Dependencies:** icons and static component data. No audio API or recorder.

#### 20. Observation Journal

- **Studio screen / source:** Observation Journal; `project/src/screens/ObservationJournal.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**; displayed entries and prompt are static, and new entries are not saved.
- **Underlying pattern:** private material capture with a prompt and lightweight composition.
- **User → system:** open the composer, type a draft, choose Save or Discard. Save merely closes the composer; it does not append the draft to `entries`. Discard closes it and clears the draft.
- **Inputs → outputs:** textarea string → no saved entry or list update.
- **State / navigation / persistence:** `composing` and `draft` are local. A saved draft remains in component state if the screen stays mounted but is not displayed as an entry; nothing is persisted across navigation/reload.
- **UI / interaction:** prompt card, dated/tagged static entries, inline composer, autosized-looking textarea, Save/Discard controls.
- **Dependencies:** local React state and static `entries` array; no notebook API or storage.

#### 21. Community feed

- **Studio screen / source:** Community; `project/src/screens/Community.tsx`.
- **Status:** **STATIC DATA**.
- **Underlying pattern:** optional sharing/discovery feed.
- **User → system:** read featured and recent posts. The plus button has no handler; there is no open-post, comment, reply, reaction, or sharing flow.
- **Inputs → outputs:** hard-coded post objects → rendered feed only.
- **State / navigation / persistence:** no feed state, account state, or persistence.
- **UI / interaction:** featured cards use an accent border; posts have author/role, type, time, and text; no engagement counts are shown.
- **Dependencies:** static array and type-color mapping. No community service or moderation tools.

#### 22. Profile / Progress / Artistic Record

- **Studio screen / source:** Profile; `project/src/screens/Profile.tsx`, `project/src/App.tsx`.
- **Status:** **STATIC DATA**.
- **Underlying pattern:** personal archive/progress summary and account destination.
- **User → system:** view a profile letter, a Craft Signature message, stats, and menu labels. Account Settings, Notifications, About Studio, and Sign out have no handlers.
- **Inputs → outputs:** fixed values → display only.
- **State / navigation / persistence:** no profile model or computed progress. All values are literal constants.
- **UI / interaction:** two-column numeric stats, quote-like signature placeholder, ruled menu rows.
- **Dependencies:** Profile tab only. No identity, settings, or progress service.

### Requested items not implemented as Studio features

#### 23. Recent takes / archive and history

- **Studio screen / source:** Recent Takes in `project/src/screens/SelfTapeStudio.tsx`; counts in `project/src/screens/Profile.tsx`; screen stack in `project/src/App.tsx`.
- **Status:** **STATIC DATA** for the displayed work/take history; the local navigation stack itself is implemented (record 05).
- **Underlying pattern:** distinguish navigation history from a durable record of work.
- **User → system:** recent takes can be read but not opened or filtered; profile counts are read-only. Back returns through screens only.
- **Inputs → outputs:** fixed take/stat objects → static list/counts; current screen sequence → in-memory back behavior.
- **State / navigation / persistence:** no durable activity timeline, archive query, or saved recently studied list. Screen history is cleared on tab changes and reload.
- **UI / interaction:** date/status labels and list rows suggest history, without record actions.
- **Dependencies:** static JSX data and App state; no history store.

#### 24. Studio Library (as a distinct destination)

- **Studio screen / source:** no screen or component with this name. The closest actual screen is Practice Library, `project/src/screens/PracticeLibrary.tsx`.
- **Status:** **SPECIFICATION ONLY** as a separately named destination; the nearest actual screen is record 10.
- **Underlying pattern:** browseable reference/learning library.
- **User → system:** no separate Studio Library action exists in the source; the Library bottom tab opens Practice Library.
- **Inputs → outputs:** none for a distinct Studio Library.
- **State / navigation / persistence:** inherited local tab navigation only.
- **UI / interaction:** do not infer additional Studio Library behavior beyond Practice Library's tool cards and category list.
- **Dependencies:** Practice Library only.

#### 25. Teacher Studio / teacher workflows

- **Studio screen / source:** no Teacher Studio screen, teacher account mode, or teacher destination exists in `project/src/`.
- **Status:** **SPECIFICATION ONLY** relative to the requested checklist; not implemented in the supplied source.
- **Underlying pattern:** teacher-facing administration/review, if such a product were specified.
- **User → system:** no teacher user action or system response exists.
- **Inputs → outputs:** none. Teacher names/roles appear as static exercise metadata; profile includes a fixed “Teacher reviews” number; Script Lab contains copy promising comments after a scene is open.
- **State / navigation / persistence:** no teacher state, class/attendance data, review records, or stored comments.
- **UI / interaction:** no teacher-facing UI or comment action.
- **Dependencies:** none in code.

#### 26. Annotation and comments

- **Studio screen / source:** only mentioned in text in `project/src/screens/ScriptLab.tsx` (“Beat tagging, objective annotation, and teacher comments…”).
- **Status:** **SPECIFICATION ONLY**.
- **Underlying pattern:** attach structured notes or discussion to selected text/context.
- **User → system:** no selection, tag, annotation, or comment action exists because no scene can be opened.
- **Inputs → outputs:** no text span, annotation object, comment, or output is created.
- **State / navigation / persistence:** none.
- **UI / interaction:** screen copy only; not an interactive feature.
- **Dependencies:** no annotation/comment model or service in the archive.

#### 27. Recording workflows

- **Studio screen / source:** visual surfaces in `SelfTapeStudio.tsx` and `VoiceStudio.tsx`.
- **Status:** **VISUAL PLACEHOLDER**.
- **Underlying pattern:** capture, review, compare, and retain media takes.
- **User → system:** no record/start/stop/play/compare action is wired.
- **Inputs → outputs:** no camera frames, audio samples, media files, or recorded takes.
- **State / navigation / persistence:** none.
- **UI / interaction:** descriptions mention camera frame guides, eye-line markers, countdown, and record/compare; actual controls are inert.
- **Dependencies:** no media APIs, permission handling, upload, playback, or media storage.

### Cross-screen interaction and data patterns

#### 28. Cards, rows, and content presentation

- **Studio screen / source:** Home, Practice Library, Craft Category, Performance Atlas, Daily Practice, Journal, Community, and Profile; `project/src/screens/*.tsx`.
- **Status:** **IMPLEMENTED** as presentation; resulting action depends on the screen (records 03, 07, 10–13, 20–22).
- **Underlying pattern:** editorial cards for featured items and compact rows for scannable collections.
- **User → system:** tap behavior is wired on some cards to navigate/open/complete; others are inert display containers.
- **Inputs → outputs:** static content objects and callbacks → card/list render, and on wired items a local transition/state update.
- **State / navigation / persistence:** no general card state or persistence.
- **UI / interaction:** image overlays, thin borders, muted surfaces, active/hover feedback, category badges, descriptions, and compact metadata.
- **Dependencies:** Tailwind classes and each screen's callback. Card styling alone does not imply the displayed action is implemented.

#### 29. Forms and editing

- **Studio screen / source:** Onboarding and Observation Journal; `project/src/screens/Onboarding.tsx`, `project/src/screens/ObservationJournal.tsx`.
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Underlying pattern:** collect a small choice or capture freeform material.
- **User → system:** onboarding selection changes local selected styling and screen context; journal textarea accepts text. Journal Save does not commit, and Discard clears the draft.
- **Inputs → outputs:** `UserType` and textarea string → local state only; no persisted record.
- **State / navigation / persistence:** React component state, no submit handler, validation, autosave, or storage.
- **UI / interaction:** selectable cards, CTA, inline textarea composer, Save/Discard controls.
- **Dependencies:** React local state and parent callback for onboarding.

#### 30. Content model and persistence behavior

- **Studio screen / source:** data in `project/src/data/atlas.ts`, `project/src/data/craft.ts`, `project/src/data/practice.ts`; state in `project/src/App.tsx` and screen components.
- **Status:** **STATIC DATA** for content; transient UI state is locally implemented.
- **Underlying pattern:** structured content modules plus local interaction state.
- **User → system:** screens read static arrays/objects and update in-memory React state for query, selection, completion, scroll, or draft.
- **Inputs → outputs:** TypeScript records → rendered screens. No user action writes a durable record.
- **State / navigation / persistence:** no database/API calls, localStorage, sessionStorage, file upload, or backend writes were found in source. The declared Supabase package is unused.
- **UI / interaction:** Atlas, craft, exercise, journal, community, profile, and take data appear credible but remain bundled examples.
- **Dependencies:** React state, local `.ts` data modules, and bundled/static image paths.

## Studio → Narrative Lab mapping

`KEEP` means the interaction abstraction can be reused with a Narrative Lab implementation. `MODIFY` means retain the idea but redesign it around narrative objects and the responsive product architecture. `DROP` means the actor-specific feature should not be carried forward. `LATER` means the pattern may be useful beyond the first usable version. “Priority” refers to product-design attention, not a decision to implement now.

| Studio feature / source status | Underlying pattern | Narrative Lab translation | Recommendation | Priority |
| --- | --- | --- | --- | --- |
| Splash / entry — partial | Immersive entry | Narrative Lab entry introducing study and making | MODIFY | Later |
| Actor-role onboarding — partial | First-run context selection | Product orientation only if it serves the agreed workflow; no actor roles | DROP | Low |
| Home — partial/static | Curated editorial front page | Home for featured study, discoveries, and continue-work context | MODIFY | High |
| Bottom navigation — implemented | Top-level destination switcher | Organize around Study / Make with responsive navigation | MODIFY | High |
| Local back stack — implemented | Contextual return path | Work → scene → beat/object/evidence with clear return points | KEEP + MODIFY | High |
| Directional transitions — implemented | Navigation direction feedback | Restrained responsive transitions with reduced-motion support | KEEP + MODIFY | Medium |
| Daily Practice — partial | Guided sequential session | Optional guided Study / reading session | MODIFY · LATER | Later |
| Exercise detail/completion — local | Focused prompt and completion action | Scene prompts or analytical checkpoints; no exercise streak | MODIFY · LATER | Later |
| Practice Library — partial | Browseable collection | Study reference shelf / atlas entry points | MODIFY | High |
| Craft categories — partial | Topic taxonomy and subnavigation | Narrative topics and mechanism pages | MODIFY | Medium |
| Performance Atlas — partial | Curated analytical archive | Story Atlas for works, scenes, mechanisms, and examples | KEEP + MODIFY | High |
| Atlas search — implemented | Deterministic metadata search | Search works and narrative entities by indexed metadata | KEEP + MODIFY | High |
| Atlas filter chips — partial | Metadata facets | Real deterministic filters for genre, period, writer, mechanism, etc. | KEEP + MODIFY | High |
| Atlas Entry — partial | Context-first analytical detail | Evidence-based Work / Scene / Character / Mechanism detail | KEEP + MODIFY | High |
| Script Lab — placeholder | Annotated text workspace | Screenplay Lab / Scene Study with text selection and linked anatomy | MODIFY | High |
| Self-Tape Studio — placeholder | Media recording and take review | No direct Narrative Lab equivalent | DROP | Low |
| Voice Studio — placeholder | Audio training session | No direct Narrative Lab equivalent | DROP | Low |
| Observation Journal — partial | Private material capture | Writer's Notebook / Material for observations, fragments, questions | MODIFY | Medium |
| Community feed — static | Optional sharing/discovery | Possible later reference exchange; no social layer in MVP | LATER | Low |
| Profile / Progress — static | Longitudinal personal record | Work / Writing Record for studied works, drafts, revisions, references | MODIFY · LATER | Later |
| Recent takes / history — static | Recent activity/archive | Recently studied, current work, and durable user history | MODIFY | Medium |
| Studio Library — absent as named | Browseable reference library | Reference Shelf; closest source analog is Practice Library | MODIFY | Medium |
| Teacher Studio — absent | Teacher administration/review | No MVP translation; Narrative Lab is not a teacher/student product | DROP | Low |
| Annotations/comments — specification only | Context-attached notes/discussion | Evidence-linked annotations and Writer Notes; comments require separate scope | MODIFY | High |
| Recording workflows — placeholders | Capture and compare media | Drop camera/self-tape/voice recording features | DROP | Low |
| Cards and rows — implemented presentation | Editorial and scannable content layout | Reusable work/scene/entity cards and structured lists | KEEP + MODIFY | Medium |
| Forms/editing — partial | Lightweight choice and capture | Persisted private notes and explicit evidence/interpretation inputs when scoped | MODIFY | Medium |
| Static content/state — source architecture | Bundled content plus transient state | Shared narrative model and persistent source/evidence-linked records | MODIFY | High |

These mappings are not one-to-one requirements. Some Studio patterns can support multiple Narrative Lab areas, and the narrative objects, parser, and analysis methodology have no equivalent in the Studio prototype.

## Studio patterns worth carrying into Narrative Lab

The source evidence column below matters: some useful ideas are working Studio behaviors; others are gaps that Narrative Lab should design independently using its own model.

| Pattern | Source evidence | Why it is useful for Narrative Lab |
| --- | --- | --- |
| Immersive entry | Working splash presentation; no account flow | Establish the reflective, cinematic tone before entering a work context. Keep optional and quick. |
| Editorial home | Working Home layout over static content | Give a current study or work a meaningful place before utility links. |
| Curated discovery | Home's featured item and horizontal Atlas row | Surface a related work, scene, or mechanism without turning Home into a control dashboard. |
| Searchable archive | Atlas text search works; facets do not | Let users find narrative objects quickly; make every displayed filter actually constrain results. |
| Contextual detail pages | Atlas Entry is implemented, though some analysis is placeholder | Place metadata and context before analytical sections; make the parent and return path clear. |
| Sequential guided sessions | Daily Practice progression works locally | Could guide a user through observe → predict → compare → record; keep optional, evidence-focused, and non-gamified. |
| Annotation alongside source | Specification-only in Studio Script Lab | Useful for connecting screenplay passages to beats, objectives, evidence, and notes; must be built around Narrative Lab's shared model. |
| Private notebook | Composer shell exists, but Save does not save | Material capture is useful for writers; implement persistence and privacy deliberately. |
| History / continue context | Only in-memory navigation and static recent examples exist | Restore a work/scene context and make studied or created material retrievable. |
| Deliberate transitions | Push/pop/fade are implemented | Help users understand movement between work, scene, anatomy, and evidence without excessive motion. |
| Completion states | Practice completion UI works locally | Confirm meaningful milestones (for example, parse ready or study note saved) without streaks, XP, or badges. |
| Cross-linking | Not implemented as entity links in Studio | Narrative Lab benefits from linking a scene to its characters, events, mechanisms, evidence, and source passage. This should follow the model, not be inferred from Studio. |
| Evidence/context presentation | Atlas provides context and image credits, but no claim-level evidence records | Narrative analysis needs source excerpts and evidence links so facts, inferences, and interpretations stay distinguishable. |

## Studio features explicitly excluded from Narrative Lab

Do not carry over actor-specific product features: voice drills and vocal training; movement training; self-tape recording, review, and submission; actor performance evaluation; acting-school enrollment/onboarding; teacher/student administration, attendance, assignment, or teacher-review workflows; actor practice categories; rehearsal streaks; XP, levels, badges, or achievement mechanics. Community is not a core MVP feature; do not add follower counts, rankings, or engagement mechanics.

The current Studio ZIP does not implement several of those named workflows, but their screen copy or checklist presence is still not a reason to add them to Narrative Lab.

## Narrative Lab conceptual feature map

This is a future product hierarchy from the supplied Narrative Lab brief, not a statement that these screens already exist or an implementation plan for this task.

```text
NARRATIVE LAB
│
├── HOME
│
├── STUDY
│   ├── Story Atlas
│   ├── Works
│   ├── Scene Study
│   ├── Character Study
│   ├── Mechanisms
│   ├── Comparisons
│   └── Reference Shelf
│
├── MAKE
│   ├── My Works
│   ├── Writing Studio
│   ├── Scene Work
│   ├── Material / Notes
│   ├── Revision
│   └── Transform
│
└── COMMON
    ├── Search
    ├── Notes
    └── History
```

These views should operate on shared narrative objects—Work, Scene, Character, Relationship, Event, Beat, Objective, Obstacle, Information, Narrative State, Theme, Motif, Setup, Payoff, Mechanism, Convention, and Evidence—rather than creating a separate copy of an object per screen. The source → parser → narrative model → structural analysis → evidence → interpretation → user action sequence remains Narrative Lab's architecture, not a Studio-derived feature.

## Inventory summary

- **30 inventory records** are documented, including cross-screen patterns and checklist areas absent from the archive.
- **7 IMPLEMENTED:** local navigation, transitions, selected focused views/completion states, text search, and card/list presentation. “Implemented” here does not mean server-backed or durable.
- **12 PARTIALLY IMPLEMENTED:** features where some visible or local interaction works but an important part is missing, including Atlas filters, data-backed history, and Journal saving.
- **4 VISUAL PLACEHOLDER:** Script Lab, Self-Tape, Voice Studio, and camera/audio capture surfaces.
- **4 STATIC DATA:** Community, Profile/Progress, recent history examples, and content/persistence as a whole.
- **3 SPECIFICATION ONLY:** a distinct Studio Library destination, Teacher Studio, and annotation/comments workflows.

Highest-value translations to consider are a curated editorial Home, responsive contextual navigation, a genuinely searchable/filtered Story Atlas, evidence-based detail pages, and a Screenplay Lab that keeps source text primary and links analysis to shared narrative objects. A private Writer's Notebook is also a useful candidate. Guided Study and the personal work archive can follow once the first usable workflow is established. This prioritization is analysis only; this inventory implements none of these features.
