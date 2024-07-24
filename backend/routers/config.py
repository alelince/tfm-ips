from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, noload

from .authentication import get_current_user
from .. import schemas, models
from ..database import get_db

router = APIRouter()

@router.get("/", status_code=200)
async def heartbeat():
    return {"status": "ok"}

@router.get("/scenarios", status_code=200)
async def list_scenarios() -> list[schemas.Scenario]:
    return schemas.Scenario.__members__.values()

@router.get("/blueprints/{scenario}", status_code=200)
async def get_blueprint(scenario: str) -> FileResponse:
    scenario = scenario.upper()
    if scenario == schemas.Scenario.ROOM.name:
        return FileResponse("img/sala.png")
    if scenario == schemas.Scenario.FLOOR.name:
        return FileResponse("img/planta.png")
    raise HTTPException(status_code=404, detail=f"unknown scenario: {scenario}")

@router.get("/campaigns", status_code=200)
async def list_campaigns(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
) -> list[schemas.AcquisitionCampaignOut]:
    try:
        return db.query(models.AcquisitionCampaign) \
            .options(noload(models.AcquisitionCampaign.points)) \
            .where(models.AcquisitionCampaign.user_id == user.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
