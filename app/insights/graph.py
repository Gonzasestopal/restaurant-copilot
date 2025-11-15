# insights/graph.py
from langgraph.graph import StateGraph, END

from .state import InsightsState
from .nodes import generate_sql_node, run_sql_node, analyze_node

def build_insights_graph():
    workflow = StateGraph(InsightsState)

    # Nodos
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("run_sql", run_sql_node)
    workflow.add_node("analyze", analyze_node)

    # Inicio
    workflow.set_entry_point("generate_sql")

    # Edges
    workflow.add_edge("generate_sql", "run_sql")
    workflow.add_edge("run_sql", "analyze")
    workflow.add_edge("analyze", END)

    # Compilar grafo
    return workflow.compile(debug=True)

graph = build_insights_graph()
