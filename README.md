# Cynbit AI Project Discovery & Lead Qualification Assistant

A proof-of-concept for the AI/ML Engineer Intern assessment with an animated, responsive Streamlit dashboard. It converts natural-language project inquiries into structured discovery information, identifies missing requirements, recommends a service category and calculates an explainable rule-based priority score.

> Important: This is an independent prototype based on publicly described business context. It is not an official Cynbit product. Sample inquiries are synthetic. The lead score is not a probability of conversion.

## Features

- Streamlit user interface.
- FastAPI endpoint (`POST /analyze`).
- Pydantic input validation.
- Requirement, industry, budget and timeline extraction.
- Service recommendation.
- Missing-information detection and follow-up questions.
- Explainable 0–100 heuristic score.
- Optional Groq LLM enrichment.
- Deterministic fallback if no LLM key is configured.
- JSON download.
- Basic pytest coverage.

## Requirements

- Python 3.10+
- pip
- Optional: Groq API key for LLM enrichment

## Local setup

```bash
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd cynbit-ai-project-discovery

python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
cp .env.example .env
```

The application works without an API key. For optional Groq enrichment, add your key to `.env` and load it before running:

```bash
export $(grep -v '^#' .env | xargs)
```

Never commit `.env`.

## Run the Streamlit application

```bash
streamlit run app.py
```

## Run the FastAPI backend

In a separate terminal, activate the same virtual environment:

```bash
uvicorn backend.main:app --reload
```

- Health: http://localhost:8000/health
- API documentation: http://localhost:8000/docs

Example API request:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"inquiry":"We need a multilingual healthcare chatbot for our website. Budget INR 200000 and launch in 2 months."}'
```

In the Streamlit sidebar, enable **Use FastAPI backend** to call the API instead of running the analyzer directly.

## Run tests

```bash
pytest -q
```

## Repository structure

```text
.
├── app.py
├── backend/
│   ├── __init__.py
│   ├── analyzer.py
│   └── main.py
├── data/
│   └── sample_leads.json
├── prompts/
│   └── lead_analysis.txt
├── reports/
│   ├── AI_Opportunity_Report.md
│   └── Technical_Approach_Report.md
├── tests/
│   └── test_analyzer.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Scoring logic

| Criterion | Maximum points |
|---|---:|
| Clear business need | 20 |
| Budget provided | 20 |
| Timeline provided | 15 |
| Requirements clarity | 25 |
| Integration or delivery detail | 10 |
| Business context | 10 |
| Total | 100 |

Priority bands: High ≥70, Medium ≥40, Low <40. The score is an illustrative inquiry-readiness heuristic, not a trained conversion prediction. Weights must be validated with business stakeholders.

## Evaluation approach

Use a manually labelled, consented and anonymized dataset. Measure field extraction precision/recall/F1, industry and service classification accuracy, missing-field detection quality, human-rated follow-up usefulness, latency and error rate. Do not claim accuracy until measured on a representative holdout set.

## Limitations

- Synthetic demonstration data only.
- No access to Cynbit's private CRM or customer records.
- Rule-based extraction is intentionally simple.
- Optional LLM enrichment depends on provider availability.
- No authentication, persistent database, CRM write-back or production security controls.
- Human review is required before customer communication, estimates or commitments.

## Deployment

For a public demo, deploy Streamlit and FastAPI as separate services, configure the API URL using Streamlit secrets/environment variables, add authentication and rate limiting, and keep provider credentials in the deployment secret manager. Do not expose an unauthenticated API with an LLM key.

## Assessment deliverables

- `reports/AI_Opportunity_Report.md`
- `reports/Technical_Approach_Report.md`
- Working Streamlit app and FastAPI API
- Sample synthetic inquiries and tests

Before submission, update this README with your own GitHub repository URL, screenshots, a short demo recording if available, and actual test results from your machine.


## UI design

The Streamlit interface includes a dark navy visual system, mint/cyan accent gradients, animated hero sheen and ambient rings, entrance transitions, pulsing status indicator, animated score bars, responsive metric cards and reduced-motion accessibility support. Animations are CSS-only and do not affect the analysis pipeline.


## Context-aware customer follow-up chat

After a project inquiry is analyzed, the interface exposes a chat area. A customer can ask follow-up questions about the same project. The conversation receives the original inquiry, the structured analysis and recent chat turns as context.

- With `GROQ_API_KEY` configured, Groq generates open-ended contextual answers.
- Without a key, a deterministic fallback answers common questions about the captured project details and clearly indicates that open-ended LLM answering is unavailable.
- The assistant must not invent prices, delivery commitments, confirmed scope or integrations. Unknown details are sent back for human confirmation.
- Chat history is held in Streamlit session state for the current browser session; this prototype does not persist it to a database.

Set `GROQ_API_KEY` in `.env`. The app loads `.env` automatically through `python-dotenv`. Never commit real API credentials.


## UI update: no backend toggle + animated 3D-style hero

The Streamlit sidebar no longer exposes the FastAPI connection toggle or backend URL. The UI calls the local analysis function directly. The API remains available separately for development and integration.

The hero now includes a CSS 3D-style scene using perspective, layered orbital rings, a shaded sphere and floating labels. This is a lightweight CSS 3D animation, not a WebGL/Three.js model; it runs without an additional graphics dependency. Reduced-motion preferences are respected.
