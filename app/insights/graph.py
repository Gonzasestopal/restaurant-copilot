# insights/graph.py
from langgraph.graph import StateGraph, END

from .state import InsightsState
from .nodes import (
    validate_question_node,
    rejection_node,
    generate_sql_node,
    run_sql_node,
    analyze_node
)

def should_continue(state: InsightsState) -> str:
    """Route based on validation result"""
    if state.get("is_valid", True):
        return "generate_sql"
    else:
        return "rejection"

def build_insights_graph():
    workflow = StateGraph(InsightsState)

    # Nodos
    workflow.add_node("validate", validate_question_node)
    workflow.add_node("rejection", rejection_node)
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("run_sql", run_sql_node)
    workflow.add_node("analyze", analyze_node)

    # Inicio: validar primero
    workflow.set_entry_point("validate")

    # Routing condicional después de validación
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "generate_sql": "generate_sql",
            "rejection": "rejection"
        }
    )

    # Flujo normal para preguntas válidas
    workflow.add_edge("generate_sql", "run_sql")
    workflow.add_edge("run_sql", "analyze")
    workflow.add_edge("analyze", END)

    # Flujo para preguntas rechazadas
    workflow.add_edge("rejection", END)

    # Compilar grafo
    return workflow.compile()

graph = build_insights_graph()
