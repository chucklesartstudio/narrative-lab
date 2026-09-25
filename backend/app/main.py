from fastapi import FastAPI

from app.schemas.narrative import Character, Scene, Work


app = FastAPI(title="Narrative Lab API")


@app.get("/")
def root():
    return {
        "name": "Narrative Lab",
        "status": "running",
    }


@app.get("/test-model")
def test_model():
    work = Work(
        id="work_001",
        title="Test Work",
        medium="screenplay",
    )

    character = Character(
        id="char_001",
        work_id=work.id,
        name="Anna",
    )

    scene = Scene(
        id="scene_001",
        work_id=work.id,
        sequence=1,
        character_ids=[character.id],
    )

    return {
        "work": work.model_dump(),
        "character": character.model_dump(),
        "scene": scene.model_dump(),
    }