# Narrative Model

## 1. Work

A complete narrative work.

Examples:
- screenplay
- film
- novel
- play
- short story
- television episode

Fields:

- id
- title
- creator
- year
- medium
- language
- genre
- source
- version

---

## 2. World

The world in which the narrative occurs.

Fields:

- locations
- institutions
- social structures
- historical period
- cultural context
- rules
- constraints
- important objects

---

## 3. Character

A participant in the narrative.

Fields:

- id
- name
- role
- description
- desires
- objectives
- beliefs
- fears
- knowledge
- secrets
- values
- capabilities
- limitations
- commitments
- decisions

Character state can change over the course of the narrative.

---

## 4. Relationship

A relationship between two or more characters.

Fields:

- id
- participants
- type
- history
- trust
- attraction
- hostility
- dependency
- power
- knowledge
- intimacy

Relationships can change over time.

---

## 5. Location

A meaningful physical or conceptual place.

Fields:

- id
- name
- type
- description
- associated characters
- associated events
- narrative function

---

## 6. Event

Something that happens in the narrative world.

Fields:

- id
- description
- participants
- location
- narrative time
- chronological position
- causal predecessors
- consequences
- visibility

Events may happen:
- on screen
- off screen
- before the narrative begins
- during the narrative
- in the future

---

## 7. Scene

A narrative unit occurring within a particular situation.

Fields:

- id
- work_id
- sequence
- location
- time
- characters
- surface activity
- objective
- obstacle
- conflict
- information
- action
- dialogue
- beats
- state_before
- state_after
- narrative_function

---

## 8. Beat

A small unit in which something changes.

A beat may change:

- information
- desire
- belief
- strategy
- power
- emotion
- relationship
- expectation
- decision

Fields:

- id
- scene_id
- order
- trigger
- action
- response
- change
- evidence

---

## 9. Objective

Something a character is actively pursuing.

Fields:

- id
- character
- description
- scope
- urgency
- visibility
- success_condition
- failure_condition

Objectives can exist at multiple levels:

- story
- sequence
- scene
- beat

---

## 10. Obstacle

Something preventing an objective from being achieved.

Fields:

- id
- objective_id
- source
- type
- severity
- known_by
- outcome

---

## 11. Information

A piece of knowledge relevant to the narrative.

Fields:

- id
- content
- source
- introduced_at
- known_by
- hidden_from
- revealed_at
- discovered_at
- misunderstood_by

---

## 12. Narrative State

The state of a character, relationship, or story at a particular point.

Possible components:

- knowledge
- desire
- belief
- emotional state
- relationship state
- power
- objective
- commitment
- uncertainty

A scene can transform one state into another.

---

## 13. Theme

A recurring conceptual question, opposition, or concern.

Fields:

- id
- question
- ideas
- oppositions
- associated characters
- associated events
- associated motifs
- appearances
- transformations

---

## 14. Motif

A recurring image, object, phrase, action, sound, situation, or idea.

Fields:

- id
- type
- description
- first_appearance
- appearances
- variations
- final_appearance

---

## 15. Setup

An element introduced with potential future significance.

Fields:

- id
- introduced_in
- content
- expected_function
- later_references
- payoff_status

---

## 16. Payoff

A later event or element that gives significance to an earlier setup.

Fields:

- id
- setup_id
- occurs_in
- relationship
- transformation

---

## 17. Narrative Mechanism

A method by which a narrative produces an effect.

Examples:

- information withholding
- delayed revelation
- forced proximity
- misrecognition
- repetition
- variation
- reversal
- escalation
- false resolution
- parallel action
- role reversal
- status change
- deadline
- pursuit
- separation
- reunion

Fields:

- id
- name
- description
- function
- variants
- examples

---

## 18. Convention

A recurring narrative practice associated with a genre, tradition, period, or form.

A convention may be:

- followed
- modified
- inverted
- subverted
- rejected

Fields:

- id
- name
- tradition
- genre
- description
- variants
- works

---

## 19. Structural Unit

A larger grouping of narrative material.

Possible levels:

- act
- movement
- sequence
- chapter
- scene
- beat

Fields:

- id
- parent
- children
- order
- function

---

## 20. Evidence

The source material supporting an observation or interpretation.

Fields:

- id
- source
- page
- line
- text_span
- observation
- claim
- confidence

Every non-trivial analytical claim should ideally have evidence.

---

# Core Principle

The system should distinguish:

FACT
- directly present in the source

INFERENCE
- derived from source evidence

INTERPRETATION
- an analytical explanation of what the material may mean or accomplish

The system should not present interpretation as fact.