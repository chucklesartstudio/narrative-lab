from typing import Optional
from pydantic import BaseModel, Field


class Work(BaseModel):
    id: str
    title: str
    creator: list[str] = Field(default_factory=list)
    year: Optional[int] = None
    medium: str
    language: Optional[str] = None
    genre: list[str] = Field(default_factory=list)
    source: Optional[str] = None
    version: Optional[str] = None


class World(BaseModel):
    id: str
    work_id: str
    historical_period: Optional[str] = None
    cultural_context: Optional[str] = None
    institutions: list[str] = Field(default_factory=list)
    social_structures: list[str] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class Location(BaseModel):
    id: str
    work_id: str
    name: str
    location_type: Optional[str] = None
    description: Optional[str] = None
    narrative_function: Optional[str] = None


class Character(BaseModel):
    id: str
    work_id: str
    name: str
    role: Optional[str] = None
    description: Optional[str] = None

    desires: list[str] = Field(default_factory=list)
    objectives: list[str] = Field(default_factory=list)
    beliefs: list[str] = Field(default_factory=list)
    fears: list[str] = Field(default_factory=list)
    values: list[str] = Field(default_factory=list)
    secrets: list[str] = Field(default_factory=list)

    capabilities: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    commitments: list[str] = Field(default_factory=list)


class Relationship(BaseModel):
    id: str
    work_id: str

    participants: list[str] = Field(default_factory=list)
    relationship_type: Optional[str] = None
    history: Optional[str] = None

    trust: Optional[float] = Field(default=None, ge=0, le=1)
    attraction: Optional[float] = Field(default=None, ge=0, le=1)
    hostility: Optional[float] = Field(default=None, ge=0, le=1)
    dependency: Optional[float] = Field(default=None, ge=0, le=1)
    power: Optional[float] = Field(default=None, ge=0, le=1)
    intimacy: Optional[float] = Field(default=None, ge=0, le=1)


class Event(BaseModel):
    id: str
    work_id: str

    description: str
    participants: list[str] = Field(default_factory=list)
    location_id: Optional[str] = None

    narrative_time: Optional[str] = None
    chronological_position: Optional[int] = None

    causal_predecessors: list[str] = Field(default_factory=list)
    consequences: list[str] = Field(default_factory=list)

    visibility: str = "unknown"


class Objective(BaseModel):
    id: str
    character_id: str
    description: str

    scope: str = "scene"
    urgency: Optional[str] = None
    visibility: str = "unknown"

    success_condition: Optional[str] = None
    failure_condition: Optional[str] = None


class Obstacle(BaseModel):
    id: str
    objective_id: str

    source: Optional[str] = None
    obstacle_type: Optional[str] = None
    severity: Optional[str] = None

    known_by: list[str] = Field(default_factory=list)
    outcome: Optional[str] = None


class Information(BaseModel):
    id: str
    work_id: str

    content: str
    source: Optional[str] = None

    introduced_at: Optional[str] = None
    revealed_at: Optional[str] = None
    discovered_at: Optional[str] = None

    known_by: list[str] = Field(default_factory=list)
    hidden_from: list[str] = Field(default_factory=list)
    misunderstood_by: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    id: str

    source_id: str
    claim: str
    observation: str

    page: Optional[int] = None
    line: Optional[int] = None

    text_span: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0, le=1)


class Beat(BaseModel):
    id: str
    scene_id: str
    order: int

    trigger: Optional[str] = None
    action: Optional[str] = None
    response: Optional[str] = None
    change: Optional[str] = None

    evidence_ids: list[str] = Field(default_factory=list)


class Scene(BaseModel):
    id: str
    work_id: str

    sequence: int

    location_id: Optional[str] = None
    narrative_time: Optional[str] = None

    character_ids: list[str] = Field(default_factory=list)

    surface_activity: Optional[str] = None

    objective_ids: list[str] = Field(default_factory=list)
    obstacle_ids: list[str] = Field(default_factory=list)

    conflict: Optional[str] = None

    information_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)

    dialogue: Optional[str] = None
    action: Optional[str] = None

    beat_ids: list[str] = Field(default_factory=list)

    state_before: dict = Field(default_factory=dict)
    state_after: dict = Field(default_factory=dict)

    narrative_function: list[str] = Field(default_factory=list)