from fastapi import APIRouter, Header, HTTPException
from app.models.schemas import Preferences
from app.services.prefs_service import get_preferences, upsert_preferences

router = APIRouter(prefix="/api", tags=["preferences"])

def _client_id(x_client_id: str | None) -> str:
    if not x_client_id:
        raise HTTPException(status_code=400, detail="Missing X-Client-Id header")
    return x_client_id

@router.get("/preferences", response_model=Preferences)
async def read_preferences(x_client_id: str | None = Header(default=None, alias="X-Client-Id")):
    client_id = _client_id(x_client_id)
    prefs = await get_preferences(client_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not set")
    return prefs

@router.put("/preferences")
async def save_preferences(prefs: Preferences, x_client_id: str | None = Header(default=None, alias="X-Client-Id")):
    client_id = _client_id(x_client_id)
    await upsert_preferences(client_id, prefs)
    return {"ok": True}
