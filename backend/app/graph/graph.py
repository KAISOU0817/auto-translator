from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import validate_config, translate_all, extract_vocab_all, dict_lookup_all, format_output

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("validate_config", validate_config)
    g.add_node("translate_all", translate_all)
    g.add_node("extract_vocab_all", extract_vocab_all)
    g.add_node("dict_lookup_all", dict_lookup_all)
    g.add_node("format_output", format_output)

    g.set_entry_point("validate_config")
    g.add_edge("validate_config", "translate_all")
    g.add_edge("translate_all", "extract_vocab_all")
    g.add_edge("extract_vocab_all", "dict_lookup_all")
    g.add_edge("dict_lookup_all", "format_output")
    g.add_edge("format_output", END)

    return g.compile()

app_graph = build_graph()
