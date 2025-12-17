from typing import Any
from app.core.db import get_pool
from app.services.normalize import normalize_headword

async def lookup_definitions(native_lang: str, target_lang: str, words: list[str]) -> dict[str, dict[str, Any]]:
    """Return dict keyed by original word -> {meaning_native, extra, found}.

    Strategy:
      1) exact match on normalized headword
      2) ILIKE fallback (cheap fuzzy)
      3) TODO: vector semantic search (pgvector) once embeddings exist
    """
    pool = await get_pool()
    pair = f"{native_lang}-{target_lang}"

    results: dict[str, dict[str, Any]] = {}
    for w in words:
        nw = normalize_headword(target_lang, w)
        row = await pool.fetchrow(
            """
            SELECT headword, definition_native, extra
            FROM dict_entries
            WHERE pair=$1 AND headword=$2
            LIMIT 1
            """,
            pair, nw,
        )
        if not row:
            # fallback: try original surface form
            row = await pool.fetchrow(
                """
                SELECT headword, definition_native, extra
                FROM dict_entries
                WHERE pair=$1 AND headword=$2
                LIMIT 1
                """,
                pair, w.strip(),
            )
        if not row:
            # fallback: ILIKE for near matches
            row = await pool.fetchrow(
                """
                SELECT headword, definition_native, extra
                FROM dict_entries
                WHERE pair=$1 AND headword ILIKE $2
                ORDER BY length(headword) ASC
                LIMIT 1
                """,
                pair, nw + "%",
            )

        if row:
            results[w] = {
                "found": True,
                "meaning_native": row["definition_native"],
                "extra": row["extra"],
            }
        else:
            results[w] = {
                "found": False,
                "meaning_native": None,
                "extra": None,
            }
    return results
