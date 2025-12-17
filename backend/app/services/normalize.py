import re

def normalize_headword(lang: str, s: str) -> str:
    s = s.strip()
    if lang in ("en", "fr", "de", "es", "it", "pt"):
        s = s.lower()
        s = re.sub(r"[“”"'`]", "", s)
        s = re.sub(r"[^a-z0-9\- ]+", "", s)
        s = re.sub(r"\s+", " ", s).strip()
    else:
        # For ja/zh/ko etc. keep mostly as-is; you can add morphology later (MeCab, Sudachi)
        s = re.sub(r"[“”"'`]", "", s).strip()
    return s
