from typing import TypedDict, Optional

class InsightsState(TypedDict, total=False):
    question: str           # pregunta original del usuario
    sql: str                # SQL generado por el modelo
    sql_result: str         # resultado bruto de la query
    analysis: str           # explicación final para el usuario
