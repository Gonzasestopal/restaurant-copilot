from typing import TypedDict, Optional

class InsightsState(TypedDict, total=False):
    question: str           # pregunta original del usuario
    is_valid: bool          # si la pregunta es válida y relacionada al negocio
    rejection_reason: str   # razón de rechazo si is_valid es False
    sql: str                # SQL generado por el modelo
    sql_result: str         # resultado bruto de la query
    analysis: str           # explicación final para el usuario
