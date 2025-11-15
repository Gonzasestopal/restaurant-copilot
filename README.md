# 🦜 Restaurant Copilot — AI Insights & Support Assistant

**Goal:** Build an AI-powered copilot for restaurants and internal Restaurant teams that can answer operational questions, summarize performance, and surface data insights from Restaurant’s backend systems.

---

## 🚀 Overview

Restaurant Copilot combines **LangChain**, **LangSmith**, and **FastAPI** to let users query Restaurant’s data in natural language.
It connects to the analytics database, runs safe SQL queries, and returns summarized insights or troubleshooting advice.

**Example queries**

- "How were sales this weekend compared to last?"
- "Which branch had the highest average ticket size yesterday?"
- "Why are printer errors increasing in Roma Norte?"

### Resultado en LangSmith Dashboard

![LangSmith Dashboard](langsmit.png)

El dashboard muestra todos los traces de las consultas ejecutadas, incluyendo:

- Las consultas SQL generadas
- Los resultados de las evaluaciones
- Métricas de rendimiento
- Metadata asociada a cada request

---

## 🧩 Architecture

![Architecture](architecture.png)

---

## ⚙️ Tech Stack

| Layer               | Tech                      | Purpose                          |
| ------------------- | ------------------------- | -------------------------------- |
| Backend API         | **FastAPI**               | REST / chat endpoint for Copilot |
| Data Store          | **PostgreSQL / Supabase** | Restaurant & orders data         |
| LLM Framework       | **LangChain**             | SQL Agent + Prompt Templates     |
| Observability       | **LangSmith**             | Tracing & evaluation of chains   |
| Frontend (optional) | **Next.js / Streamlit**   | Simple chat UI or dashboard      |

---

## 🧱 Database Model (Analytics Subset)

| Table                | Key Fields                                                             | Purpose                  |
| -------------------- | ---------------------------------------------------------------------- | ------------------------ |
| `restaurants`        | `id`, `name`, `location`, `timezone`                                   | Context for queries      |
| `orders`             | `id`, `restaurant_id`, `total`, `payment_type`, `status`, `created_at` | Core sales data          |
| `order_items`        | `order_id`, `menu_item_id`, `quantity`, `total_price`                  | Item-level metrics       |
| `menu_items`         | `id`, `restaurant_id`, `name`, `category`, `price`                     | Menu catalog             |
| `daily_sales`        | `restaurant_id`, `day`, `total_sales`, `avg_ticket`                    | Pre-aggregated analytics |
| `metrics_dictionary` | `metric_key`, `description`, `aggregation`                             | Improves LLM accuracy    |

---

## 🧠 How It Works

1. **User asks a question** through the dashboard or API.
2. **LangChain SQL Agent** translates the natural-language prompt into a safe SQL query.
3. The agent executes the query via the analytics DB and returns raw results.
4. **LangChain** formats the response into natural language (and optional charts).
5. **LangSmith** logs the trace for debugging / evaluation.

---

## 🧰 Local Setup

```bash
# clone
git clone https://github.com/yourusername/Restaurant-copilot
cd Restaurant-copilot

# create virtual env
python -m venv venv && source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run Postgres (or use Supabase)
docker compose up -d

# launch API
uvicorn app.main:app --reload
```

Environment variables (`.env`):

```
DATABASE_URL=postgresql+psycopg2://user:pass@localhost/Restaurant
OPENAI_API_KEY=sk-...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=Restaurant-copilot
```

---

## 🔍 Example Request

```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"query": "Show me total sales per branch this week"}'
```

**Response**

```json
{
  "sql": "SELECT branch_id, SUM(total) AS sales FROM orders WHERE created_at >= NOW() - INTERVAL '7 days' GROUP BY branch_id;",
  "result": [
    { "branch_id": 1, "sales": 12500.5 },
    { "branch_id": 2, "sales": 9800.75 }
  ],
  "summary": "Branch 1 led sales this week with MXN 12.5 K."
}
```

---

## 🧮 LangSmith Tracing

Each query execution is logged to LangSmith for inspection and evaluation.
You can view traces at [smith.langchain.com](https://smith.langchain.com).

---

## 📊 Dataset Evaluation

The project includes a script to evaluate the copilot's performance using LangSmith datasets. This allows you to test the system against a set of predefined questions and analyze the results.

### What it does

The `run_datasets.py` script:

- Connects to LangSmith and loads a dataset of test questions
- Sends each question to your local API endpoint (`/ask`)
- Records all responses and traces in LangSmith for analysis
- Generates evaluation metrics and comparisons in the LangSmith dashboard

### How to run

1. **Ensure the API is running**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Update the script** (if needed):

   - Edit `run_datasets.py` and update the `dataset_name` to match your LangSmith dataset
   - Verify the `API_URL` points to your running API (default: `http://localhost:8000/ask/`)

3. **List available datasets**:
   The script will print all available datasets when you run it.

4. **Execute the evaluation**:

   ```bash
   python run_datasets.py
   ```

5. **View results**:
   - Check the console output for progress
   - Visit [smith.langchain.com](https://smith.langchain.com) to see detailed traces and metrics
   - Results are saved under the project name specified in the script (default: `restaurant-copilot-dataset-1`)

### Creating a dataset

You can create a dataset in LangSmith by uploading a JSONL file (like `dataset.jsonl`) with the format:

```json
{"inputs": {"question": "¿Qué día tuve más ventas?"}}
{"inputs": {"question": "¿Cuál fue el ticket promedio esta semana?"}}
```

---

## 🧩 Next Steps

- [ ] Add branch/location filtering.
- [ ] Integrate dashboard visuals (Plotly / Recharts).
- [x] Implement LangSmith evaluation datasets.
- [ ] Add user feedback loop for reinforcement.

---

## ⚠️ Disclaimer

This is an internal prototype for educational and operational use within Restaurant Software.
Do not expose production data without proper access controls and review.

---

## 👤 Author

**Gonzalo Sestopal**
📧 `gonzasestopal@gmail.com`
🧠 FastAPI • LangChain • PostgreSQL • MLOps
