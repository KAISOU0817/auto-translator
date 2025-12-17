from fastapi import APIRouter, Header, HTTPException
from app.models.schemas import TranslateRequest, TranslateResponse, VocabItem
from app.services.prefs_service import get_preferences
from app.graph.graph import app_graph

router = APIRouter(prefix="/api", tags=["translate"])

def _client_id(x_client_id: str | None) -> str:
    if not x_client_id:
        raise HTTPException(status_code=400, detail="Missing X-Client-Id header")
    return x_client_id

@router.post("/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest, x_client_id: str | None = Header(default=None, alias="X-Client-Id")):
    client_id = _client_id(x_client_id)
    prefs = await get_preferences(client_id)
    if not prefs:
        raise HTTPException(status_code=400, detail="Preferences not set. Call PUT /api/preferences first.")

    state = {
        "input_text": req.text,
        "native_lang": prefs.native_lang,
        "target_langs": prefs.target_langs,
    }
    out = await app_graph.ainvoke(state)
    payload = out.get("output", {})
    # Pydantic mapping for vocab items
    vocab = {}
    for lang, items in (payload.get("vocab") or {}).items():
        vocab[lang] = [VocabItem(**it) for it in items]
    return TranslateResponse(translations=payload.get("translations") or {}, vocab=vocab)
