# CreditRisk Multi-Agent

LangGraph multi-agent system for credit-risk assessment.

The supervisor routes each case through research, credit analysis, and policy review, then returns a score and recommendation.

## Layout

```
agents/          Supervisor, research, analyst, reviewer
graph/           LangGraph state, routing, and workflow
tools/           Financial, database, research, python, credit tools
mcp_servers/     MCP wrappers for research, finance, and database tools
memory/          Short-term, long-term, and retrieval helpers
models/          PD/risk scoring model
database/        SQLite schema and loader
data/            Sample borrowers, products, and policy docs
api/             FastAPI service
frontend/        Streamlit UI
evaluation/      Golden cases
tests/           Unit and graph smoke tests
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Run a local assessment

```powershell
python main.py --borrower-id B001 --product-id P200
```

## API and UI

```powershell
uvicorn api.main:app --reload
streamlit run frontend/app.py
```

## Tests and evaluation

```powershell
pytest
python evaluation/evaluate.py
python -m models.train_model
```

## Sample IDs

| Borrower | Notes              | Product | Type            |
|----------|--------------------|---------|-----------------|
| B001     | Strong consumer    | P200    | Personal loan   |
| B003     | SME retail         | P300    | Working capital |
| B004     | Weak credit        | P100    | Mortgage        |
