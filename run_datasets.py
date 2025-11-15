import requests
from dotenv import load_dotenv
from langsmith import Client, evaluate

load_dotenv()

client = Client()

API_URL = "http://localhost:8000/ask"

def api_wrapper(example):
    inputs = example.get("inputs") or example
    q = inputs.get("question")

    # Output fijo para asegurar la columna "sql"
    outputs = {
        "sql": None
    }

    # Llamada API
    try:
        r = requests.post(API_URL, json={"query": q}, timeout=120)
        raw = r.text
    except Exception as e:
        outputs["sql"] = f"API ERROR: {str(e)}"
        return {"outputs": outputs}

    # Parseo JSON
    try:
        data = r.json()
    except Exception:
        outputs["sql"] = f"INVALID JSON: {raw}"
        return {"outputs": outputs}

    # Caso exitoso: poner el SQL real
    outputs["sql"] = data.get("sql")

    return {"outputs": outputs}


# =============================
# RUN
# =============================

EVAL_DATASET = "ds-plaintive-prosecutor-50"

print("🚀 Ejecutando evaluación con dataset:", EVAL_DATASET)

results = evaluate(
    api_wrapper,
    EVAL_DATASET
)

print("🎉 Evaluación completada con éxito")
