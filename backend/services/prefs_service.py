from app.core.db import get_pool
from app.models.schemas import Preferences

async def get_preferences(client_id: str) -> Preferences | None:
    pool = await get_pool()
    row = await pool.fetchrow(
        "SELECT native_lang, target_langs FROM user_prefs WHERE client_id=$1",
        client_id,
    )
    if not row:
        return None
    return Preferences(native_lang=row["native_lang"], target_langs=list(row["target_langs"]))

async def upsert_preferences(client_id: str, prefs: Preferences) -> None:
    pool = await get_pool()
    await pool.execute(
        """
        INSERT INTO user_prefs (client_id, native_lang, target_langs)
        VALUES ($1, $2, $3)
        ON CONFLICT (client_id)
        DO UPDATE SET native_lang=EXCLUDED.native_lang,
                      target_langs=EXCLUDED.target_langs,
                      updated_at=now()
        """,
        client_id,
        prefs.native_lang,
        prefs.target_langs,
    )
