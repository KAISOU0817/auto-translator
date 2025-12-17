from typing_extensions import TypedDict
from typing import Dict, List, Optional, Any

class AgentState(TypedDict, total=False):
    input_text: str
    native_lang: str
    target_langs: List[str]

    translations: Dict[str, str]           # {"en": "...", "ja": "..."}
    vocab_candidates: Dict[str, List[dict]] # {"en": [{"word":..,"reason":..}], ...}
    definitions: Dict[str, Dict[str, dict]] # {"en": {"word": {...}}, ...}

    # Final merged result
    output: Any
