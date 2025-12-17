from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Preferences(BaseModel):
    native_lang: str = Field(..., description="User native language (e.g., zh, en, ja)")
    target_langs: List[str] = Field(..., min_length=2, max_length=2, description="Exactly two target languages")

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")

class VocabItem(BaseModel):
    word: str
    reason: Optional[str] = None
    meaning_native: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class TranslateResponse(BaseModel):
    translations: Dict[str, str]
    vocab: Dict[str, List[VocabItem]]
