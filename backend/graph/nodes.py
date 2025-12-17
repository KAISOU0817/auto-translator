import asyncio
from app.graph.state import AgentState
from app.services.llm_service import translate, extract_vocab
from app.services.dict_service import lookup_definitions

def validate_config(state: AgentState) -> AgentState:
    native = state["native_lang"]
    targets = state["target_langs"]
    if len(targets) != 2:
        raise ValueError("target_langs must contain exactly 2 languages")
    if len(set(targets)) != 2:
        raise ValueError("target_langs must be two different languages")
    if native in targets:
        raise ValueError("target_langs must not include native_lang")
    return state

async def translate_all(state: AgentState) -> AgentState:
    text = state["input_text"]
    targets = state["target_langs"]

    async def one(lang: str):
        t = await translate(text, target_lang=lang)
        return lang, t

    pairs = await asyncio.gather(*[one(lang) for lang in targets])
    translations = {lang: t for lang, t in pairs}
    return {"translations": translations}

async def extract_vocab_all(state: AgentState) -> AgentState:
    native = state["native_lang"]
    translations = state.get("translations", {})
    targets = state["target_langs"]

    async def one(lang: str):
        items = await extract_vocab(translations.get(lang, ""), target_lang=lang, native_lang=native)
        return lang, items

    pairs = await asyncio.gather(*[one(lang) for lang in targets])
    vocab_candidates = {lang: items for lang, items in pairs}
    return {"vocab_candidates": vocab_candidates}

async def dict_lookup_all(state: AgentState) -> AgentState:
    native = state["native_lang"]
    targets = state["target_langs"]
    vocab_candidates = state.get("vocab_candidates", {})

    definitions_by_lang = {}
    for lang in targets:
        words = [it.get("word","").strip() for it in vocab_candidates.get(lang, []) if it.get("word")]
        # de-dup while preserving order
        seen = set()
        words = [w for w in words if not (w in seen or seen.add(w))]
        defs = await lookup_definitions(native, lang, words)
        definitions_by_lang[lang] = defs

    return {"definitions": definitions_by_lang}

def format_output(state: AgentState) -> AgentState:
    translations = state.get("translations", {})
    vocab_candidates = state.get("vocab_candidates", {})
    definitions = state.get("definitions", {})
    targets = state["target_langs"]

    vocab_out = {}
    for lang in targets:
        items = []
        defs = definitions.get(lang, {})
        for it in vocab_candidates.get(lang, []):
            w = it.get("word")
            if not w:
                continue
            d = defs.get(w, {})
            items.append({
                "word": w,
                "reason": it.get("reason"),
                "meaning_native": d.get("meaning_native"),
                "extra": d.get("extra"),
                "found": d.get("found", False),
            })
        vocab_out[lang] = items

    # If you truly want ONLY vocab output, you can drop translations here.
    return {"output": {"translations": translations, "vocab": vocab_out}}
