# insights/nodes.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .state import InsightsState
from app.insights.db import run_sql_raw
from app.config import settings

import datetime
import uuid
import decimal
from typing import Any, Dict, List

#
# --- SAFE CONVERSION HELPERS ---
#

def convert_value(v: Any) -> Any:
    """Convert psycopg2 native types into JSON-safe Python types."""

    if isinstance(v, decimal.Decimal):
        return float(v)

    if isinstance(v, datetime.datetime):
        return v.isoformat()

    if isinstance(v, datetime.date):
        return v.isoformat()

    if isinstance(v, datetime.time):
        return v.isoformat()

    if isinstance(v, uuid.UUID):
        return str(v)

    if isinstance(v, dict):
        return {k: convert_value(sub) for k, sub in v.items()}

    if isinstance(v, (list, tuple)):
        return [convert_value(item) for item in v]

    return v


def format_sql_result(result: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert psycopg2 RealDictCursor rows to JSON-safe Python dicts."""
    formatted = []
    for row in result:
        clean_row = {key: convert_value(value) for key, value in row.items()}
        formatted.append(clean_row)
    return formatted


#
# --- LLM ---
#

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    api_key=settings.openai_api_key
)


#
# --- SQL GENERATION PROMPT ---
#

sql_prompt = PromptTemplate.from_template(
    """
Eres un analista de datos experto en Parrot.

Tu base de datos TIENE EXCLUSIVAMENTE las siguientes tablas y columnas:

-----------------------------------------------------------------------
TABLE: restaurants
-----------------------------------------------------------------------
id (integer, PK)
name (string)
location (string)
timezone (string)
created_at (timestamp)
updated_at (timestamp)

-----------------------------------------------------------------------
TABLE: menu_items
-----------------------------------------------------------------------
id (integer, PK)
restaurant_id (integer, FK -> restaurants.id)
name (string)
category (string)
price (numeric)
created_at (timestamp)
updated_at (timestamp)

-----------------------------------------------------------------------
TABLE: orders
-----------------------------------------------------------------------
id (integer, PK)
restaurant_id (integer, FK -> restaurants.id)
total (numeric)
payment_type (string: 'cash' | 'card' | 'digital')
status (string: 'pending' | 'confirmed' | 'preparing' | 'ready' |
                 'completed' | 'cancelled')
created_at (timestamp)
updated_at (timestamp)

-----------------------------------------------------------------------
TABLE: order_items
-----------------------------------------------------------------------
id (integer, PK)
order_id (integer, FK -> orders.id)
menu_item_id (integer, FK -> menu_items.id)
quantity (integer)
total_price (numeric)
created_at (timestamp)

-----------------------------------------------------------------------
TABLE: daily_sales
-----------------------------------------------------------------------
id (integer, PK)
restaurant_id (integer, FK -> restaurants.id)
day (date)
total_sales (numeric)
avg_ticket (numeric)
created_at (timestamp)
updated_at (timestamp)

-----------------------------------------------------------------------
TABLE: metrics_dictionary
-----------------------------------------------------------------------
id (integer, PK)
metric_key (string, unique)
description (string)
aggregation (string)
created_at (timestamp)
updated_at (timestamp)

-----------------------------------------------------------------------
REGLAS IMPORTANTES:
-----------------------------------------------------------------------
- SOLO puedes generar SQL usando estas tablas y columnas.
- NO inventes tablas ni columnas.
- NO generes SELECT 1 o queries triviales.
- NO generes código en bloques ``` ni ```sql.
- NO generes textos, solo SQL plano.
- SOLO SELECT. Prohibido UPDATE/DELETE/INSERT/DROP.
- Si la pregunta NO puede responderse con este schema,
  devuelve EXACTAMENTE:

    SELECT 'No puedo responder esta pregunta con el schema disponible' AS error;

-----------------------------------------------------------------------
Pregunta del usuario:
{question}
"""

)

sql_chain = sql_prompt | llm | StrOutputParser()


def clean_sql(raw: str) -> str:
    return (
        raw.replace("```sql", "")
           .replace("```", "")
           .replace("`", "")
           .strip()
    )


def generate_sql_node(state: InsightsState) -> InsightsState:
    raw_sql = sql_chain.invoke({
        "question": state["question"]
    })

    sql = clean_sql(raw_sql)
    return {**state, "sql": sql}


#
# --- EXECUTE SQL NODE ---
#

def run_sql_node(state: InsightsState) -> InsightsState:
    sql = state["sql"]

    try:
        rows = run_sql_raw(sql)               # psycopg2 RealDictCursor
        formatted = format_sql_result(rows)   # convert cleanly
    except Exception as e:
        formatted = [{"error": str(e)}]

    return {**state, "sql_result": formatted}


#
# --- ANALYSIS PROMPT ---
#

analysis_prompt = PromptTemplate.from_template(
    """
Eres un analista senior de negocio.

Pregunta original:
{question}

Resultados de la consulta SQL:
{sql_result}

Escribe una respuesta clara y accionable para un usuario de negocio:
- Resume los datos
- Explica tendencias
- Señala anomalías si existen
- Da recomendaciones concretas
"""
)

analysis_chain = analysis_prompt | llm | StrOutputParser()


def analyze_node(state: InsightsState) -> InsightsState:
    analysis = analysis_chain.invoke({
        "question": state["question"],
        "sql_result": state["sql_result"]
    })
    return {**state, "analysis": analysis}
