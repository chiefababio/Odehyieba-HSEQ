# AI Safety Incident Analysis API

This is a FastAPI-based backend for analyzing safety incidents using AI. It utilizes OpenAI's GPT model to determine root causes, underlying causes, and suggest corrective actions.

## 🔧 Features
- AI-driven incident analysis
- Stores results in a SQLite database
- REST API for analysis and retrieval
- CORS enabled for frontend interaction

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Running the API Locally

```bash
uvicorn main:app --reload
```

## 🌍 Deployment

To deploy on platforms like Railway or Heroku:

1. Push this project to GitHub.
2. Connect GitHub repo to Railway/Heroku.
3. Set `OPENAI_API_KEY` in the environment variables.

## 📬 API Endpoints

- `POST /api/analyze` – Analyze a new safety incident
- `GET /api/incidents` – Get all analyzed incidents

