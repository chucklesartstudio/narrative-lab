# Studio-Derived Design System

## Purpose and scope

This document records reusable visual and interaction principles observed in the attached Studio prototype and maps them to Narrative Lab. Studio is a reference system for presentation and interaction. Its actor-training information architecture, data, and feature set are not Narrative Lab's architecture.

The prototype was inspected from `project-bolt-sb1-tmoqsywr.zip`, particularly `src/App.tsx`, `src/index.css`, `tailwind.config.js`, `src/components/`, and the screens in `src/screens/`. The implementation is a Vite + React + TypeScript application styled with Tailwind CSS. Its app-level navigation is a local screen state and history stack, and its outer layout is capped at 430px. The observations below distinguish behavior actually present in that source from placeholder screens and concepts supplied by the Narrative Lab brief.

## Reusable visual primitives

### Color and surfaces

Studio defines a restrained dark palette in `tailwind.config.js`:

| Role | Studio token | Value |
| --- | --- | --- |
| Background | `studio-bg` | `#17181C` |
| Raised card | `studio-card` | `#22242A` |
| Secondary surface | `studio-surface` | `#1D1F24` |
| Fine border | `studio-border` | `#2E3038` |
| Primary text | `studio-ivory` | `#F4F2EF` |
| Secondary text | `studio-gray` | `#B5B7BC` |
| Muted metadata | `studio-taupe` | `#857A6A` |
| Accent | `studio-copper` | `#C86A4A` |

Cards use a slight surface lift and thin border; most corners are square or only lightly rounded. Copper is used for selected states, calls to action, small labels, and dividers rather than large areas. The olive, amber, and blue tones are secondary category/status colors in the prototype, not part of the core palette.

For Narrative Lab, these values are starting references, as specified in the brief. Keep contrast and meaning clear; use accent colors consistently for selection, evidence status, or other defined states rather than decorating every element.

### Typography and hierarchy

The prototype pairs Inter/system sans text with Roboto Condensed/Barlow Condensed for compact labels and metadata, and Playfair Display/Georgia for editorial display and occasional italic text (`index.html`, `tailwind.config.js`). It uses uppercase, letter-spaced section labels as landmarks; metadata is small and condensed; titles and selected quotations use a larger editorial face. Body copy remains a readable sans serif.

Narrative Lab can use this role-based hierarchy to distinguish work metadata, scene text, narrative-object labels, annotations, evidence, and interpretation. The exact fonts are not required; the hierarchy is the reusable principle.

### Image presentation and layout details

Studio's Home and entry page place text over large images using dark gradient overlays. The detail page fades its title block into the lower edge of its hero image. Borders, short rules, restrained card fills, and generous vertical gaps separate editorial sections. These are useful for a curated work or reference entry when imagery is available and meaningful.

The prototype's fixed 430px app width, mobile-only bottom navigation, and dense single-column assumptions are implementation constraints, not patterns to carry forward. Narrative Lab is specified to support a desktop analytical workspace, reduced-pane tablet layouts, and sequential touch-friendly phone navigation.

## Reusable motion patterns

Observed in `src/App.tsx`, `src/components/ScreenTransition.tsx`, `src/index.css`, and individual screens:

- Initial content and section groups enter in a staged fade with a small vertical offset and staggered delays.
- Forward screen changes fade in while shifting slightly from the right; back navigation uses a smaller shift from the left; tab changes fade without directional travel.
- The Home hero image uses a slow scale and horizontal pan. This is applied as ambient image motion rather than movement on controls.
- Pressable cards and buttons use restrained color, border, or scale feedback, generally around a 0.98 scale on press.
- A small set of explicit completion states uses color and icon changes rather than celebratory effects.

Carry forward the restrained pacing and make navigation direction legible. Keep motion short and subtle, avoid bounce or gamification, and provide a reduced-motion path when implementing these patterns in Narrative Lab. Loading and parsing states should name the work underway (for example, parsing, indexing scenes, or mapping characters) rather than rely on an unexplained spinner; that is a Narrative Lab requirement from the brief, not a behavior implemented in this Studio prototype.

## Reusable navigation patterns

`src/App.tsx` keeps the current screen and a local history stack. Screen-level actions push a screen, a back control pops to the previous screen, and switching a bottom tab resets that stack and fades to the selected tab's root. Nested Atlas and category pages retain an explicit contextual back label. Some screens hide the bottom bar to focus on onboarding, detail, or session flows.

Useful principles for Narrative Lab:

- Make the parent context visible and provide a clear return path from a work, scene, or analysis detail.
- Treat movement between a work, scene, beat, character, relationship, mechanism, and evidence as navigation through related levels of one narrative object.
- Distinguish opening a contextual detail from replacing the current analytical context.
- Use a wider desktop navigation and pane model, tablet drawers/sheets, and sequential phone navigation. Do not reproduce Studio's five-tab bar.

The prototype does not use a router for its screen flow, does not demonstrate URL-addressable state, and does not persist the navigation history. Its stack is an interaction reference, not an implementation to copy wholesale.

## Reusable content-presentation patterns

### Curated home

Studio Home leads with a featured study, then a horizontally browsable set of archive items, then personal practice and journal entry points. A section label and editorial image establish context before utility. This supports the brief's principle of an editorial front page rather than a grid of dashboard actions. Narrative Lab should define its own featured study, atlas discovery, and current-work sections; these exact Studio sections are not requirements.

### Searchable archive

`PerformanceAtlas.tsx` presents a search field, filter chips, a result count, and a compact list with image, title, person, year, and short curatorial copy. Search filters by actor, film, director, and tags. The filter-chip state is displayed but is not applied to the result calculation in this source, so metadata filtering is a visible pattern but not a completed behavior here. Narrative Lab should begin with deterministic filtering over its own metadata, as specified by the brief.

### Editorial detail

`AtlasEntry.tsx` is the strongest content pattern: a large image; a compact section label; title and metadata; a short curatorial introduction; then a sequentially read analysis with clear labels, fine dividers, and selected emphasized text. Its observed sections move from synopsis and context through scene-level analysis to a conclusion and reflection prompts. It also changes the floating header after scrolling and includes image credit.

Translate the sequencing and hierarchy to narrative-specific work, scene, character, mechanism, or reference entries. Keep each observation tied to evidence and distinguish source fact, inference, and interpretation according to Narrative Lab's model. Studio's evaluative wording and actor-oriented analytical fields are not the Narrative Lab ontology.

### Horizontal discovery and section labels

Studio uses one horizontal row for secondary discoveries on Home and compact uppercase labels to mark page hierarchy. Use horizontal browsing selectively for related works, scenes, or mechanisms; preserve ordinary desktop lists and grids where they scan better. Reuse section labels as structural landmarks, not as a substitute for accessible headings.

## Reusable components and interaction models

### Patterns that are implemented in the prototype

- **Screen transition wrapper:** `ScreenTransition.tsx` renders push, pop, and fade entry motions from a direction prop.
- **Explicit back and tab controls:** screen-level callbacks and `BottomNav.tsx` provide visible navigation actions and active-tab feedback.
- **Search input and filter-chip presentation:** `PerformanceAtlas.tsx` has working text search and visible filter state; only the text search affects results.
- **Inline journal composer:** `ObservationJournal.tsx` opens a textarea and offers Save and Discard actions. The entries are hard-coded; Save closes the composer but does not append or persist the draft.
- **Sequential guided session:** `DailyPractice.tsx` gates later exercises on earlier completion, marks an item complete, advances to the next available item, and presents a completion state. This is a useful pattern for an optional, non-gamified guided reading or study flow.
- **Editorial analysis sections:** `AtlasEntry.tsx` composes clearly labelled content sections with staggered reveal and divider treatments.

### Screens that are placeholders or mostly static

`ScriptLab.tsx` displays an upload panel and demonstration-scene cards, but the upload and scene buttons have no handlers and no screenplay workspace is implemented. It therefore does not provide reusable selection, highlighting, annotation, or screenplay-reading behavior; those are desired Narrative Lab interactions described by the brief, not features extracted from working Studio code.

Community, Profile, Self-Tape Studio, and Voice Studio are primarily hard-coded presentation examples with inert controls. The prototype data in `src/data/atlas.ts`, `src/data/craft.ts`, and `src/data/practice.ts` is static local content. Treat these screens and datasets as visual/context examples only.

## Narrative Lab translations

| Studio pattern or feature | Narrative Lab translation | Scope guidance |
| --- | --- | --- |
| Performance Atlas | Work Atlas, then scene and mechanism entries | Analytical, narrative-specific content with evidence; not performance reviews. |
| Script Lab concept | Screenplay Lab / Scene Study | A screenplay remains primary; selection, annotations, evidence, and anatomy should use Narrative Lab's shared narrative model. Studio's source screen does not implement these behaviors. |
| Observation Journal | Writer's Notebook / Material | Private observations, fragments, questions, references, and ideas; no social feed. |
| Craft categories | Narrative topics and mechanism pages | Organize by concepts such as conflict, information, time, relationship, reversal, or transformation when supported by the product model. |
| Profile and artistic record | Work and writing record | Archive works, study, drafts, revisions, references, and notes; do not import scores or gamified progress. |
| Daily practice | Optional study or reading session | A guided observe / predict / reveal / compare / note sequence may be useful later; it is not an MVP requirement on its own. |
| Community | Possible future reference or discussion layer | Not part of the core MVP. Do not import follower counts, ranking, or engagement mechanics. |

The brief identifies two future modes, **Study** and **Make**, but explicitly says not to build all conceptual areas at once. Use them as product-level organizing ideas only after scope is set; they do not replace the existing narrative data model.

## Explicit exclusions

Do not bring over actor-specific terminology or features: acting exercises, voice or movement training, self-tape workflows, teacher/student workflows, acting-school onboarding, rehearsal streaks, XP, levels, badges, performance evaluation, the 430px mobile-only layout, or Studio's five-tab navigation. Do not copy Studio screens or let a visual component dictate Narrative Lab's ontology.

## Architectural boundary

The Narrative Lab brief defines the system flow as:

```text
SOURCE → PARSER → NARRATIVE MODEL → STRUCTURAL ANALYSIS → EVIDENCE → INTERPRETATION → USER ACTION
```

The interface is a view over shared narrative objects. A work, scene, character, beat, mechanism, or evidence record should be reusable in the Atlas, Scene Study, Comparison, Writing Studio, or Revision contexts without duplicating the underlying entity. This is consistent with the existing `docs/architecture/narrative-model.md` principle that non-trivial analytical claims should be supported by evidence and that fact, inference, and interpretation remain distinct.

## Source limitations

This document records an inspection of the provided Studio prototype source. Its visual patterns and a few interaction flows are implemented, but some named screens are stubs, sample data is static, some controls are inert, and the apparent Atlas filters are not connected to filtering logic. The prototype is narrowly constrained to a mobile-width layout. These limitations should be kept in mind when borrowing patterns; no Studio component or product feature should be assumed production-ready for Narrative Lab.
