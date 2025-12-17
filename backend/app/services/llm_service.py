import json
from typing import Any
from openai import AsyncOpenAI
from app.core.config import settings

def _client() -> AsyncOpenAI:
    kwargs: dict[str, Any] = {"api_key": settings.openai_api_key}
    if settings.llm_base_url:
        kwargs["base_url"] = settings.llm_base_url
    return AsyncOpenAI(**kwargs)

async def translate(text: str, target_lang: str) -> str:
    """Translate `text` into `target_lang` and return translation only."""
    client = _client()
    prompt = (
        "You are a professional translator. "
        f"Translate the following text into {target_lang}. "
        "Keep meaning, context, and natural expression. "
        "Return ONLY the translated text."
    )
    resp = await client.chat.completions.create(
        model=settings.llm_model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    return (resp.choices[0].message.content or "").strip()

async def extract_vocab(translated_text: str, target_lang: str, native_lang: str) -> list[dict[str, Any]]:
    """Extract potentially difficult vocabulary for a learner with `native_lang` learning `target_lang`.

    Returns: list of {word, reason}
    """
    client = _client()
    system = (
        "You are a language-learning assistant.
"
        f"The learner's native language is {native_lang}. The learner is studying {target_lang}.
"
        "From the provided sentence, list vocabulary that a typical learner might NOT know.
"
        "Rules:
"
        "- Exclude basic function words (articles, particles, very basic verbs)
"
        "- Prefer content words (nouns, verbs, adjectives, set phrases)
"
        "- Return JSON ONLY in this schema:
"
        "  {"items": [{"word": "...", "reason": "..."}, ...]}
"
        "No extra keys, no markdown."
    )
    resp = await client.chat.completions.create(
        model=settings.llm_model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": translated_text},
        ],
        response_format={"type": "json_object"},
    )
    raw = (resp.choices[0].message.content or "").strip()
    try:
        data = json.loads(raw)
        items = data.get("items", [])
        out = []
        for it in items:
            word = (it.get("word") or "").strip()
            if not word:
                continue
            out.append({"word": word, "reason": (it.get("reason") or "").strip() or None})
        return out
    except Exception:
        # very defensive fallback
        return []
