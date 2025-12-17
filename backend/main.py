from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.db import close_pool
from app.routers.preferences import router as prefs_router
from app.routers.translate import router as translate_router

app = FastAPI(title="Multilingual Translator + Vocab Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefs_router)
app.include_router(translate_router)

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.on_event("shutdown")
async def _shutdown():
    await close_pool()
