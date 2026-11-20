# Technical Approach Report
## AI-Powered Project Discovery and Lead Qualification Assistant

## 1. Objective

Build a working prototype that accepts a customer project inquiry and returns structured project information, missing requirements, recommended service, an explainable priority score and a discovery brief.

## 2. Architecture

```text
Customer inquiry
      |
      v
Streamlit user interface
      |
      v
FastAPI endpoint (optional API mode)
      |
      v
Input validation (Pydantic)
      |
      v
Requirement extraction
  |               |
  |               +--> Optional Groq LLM enrichment
  |
  +--> Deterministic extraction fallback
      |
      v
Rule-based lead scoring
      |
      v
Service recommendation + missing fields
      |
      v
Structured JSON response
      |
      v
Discovery summary and downloadable result
```

## 3. Technology Choices

| Layer | Technology | Reason |
|---|---|---|
| Language | Python | Rapid prototyping and broad ML ecosystem |
| UI | Streamlit | Fast interactive demo |
| API | FastAPI | Typed request/response API and OpenAPI docs |
| Validation | Pydantic | Structured input and schema validation |
| LLM | Groq API (optional) | Low-latency hosted inference for enrichment |
| Baseline NLP | Python rules and regular expressions | Transparent fallback and no-key demo |
| Tests | pytest | Repeatable functional checks |

The app works without an API key using deterministic extraction. If `GROQ_API_KEY` is configured, optional LLM enrichment is attempted. The score remains rule-based in this PoC.

## 4. Data Pipeline

1. Receive the customer inquiry.
2. Validate input length and type.
3. Identify industry and project type.
4. Extract budget and timeline when present.
5. Detect requirements and integrations.
6. Identify missing information.
7. Calculate an explainable score.
8. Generate follow-up questions and project brief.
9. Return a JSON result to the UI.

The sample data is synthetic and must not be interpreted as actual Cynbit customer data.

## 5. Prompt Engineering

The prompt:
- Defines the model as a project discovery assistant.
- Treats customer input as untrusted data.
- Requires evidence-grounded extraction.
- Prohibits invented budget, timelines and integrations.
- Separates extracted facts from recommendations.
- Requests missing information and follow-up questions.
- Restricts recommendations to a known service taxonomy.

Temperature is set low to encourage consistent extraction. Structured JSON output is requested. Production should enforce a formal schema and retry/repair strategy for malformed responses.

## 6. Lead Scoring

The PoC uses a transparent heuristic score out of 100:
- Clear business need: 20 points.
- Budget provided: 20 points.
- Timeline provided: 15 points.
- Requirements clarity: up to 25 points.
- Integration or delivery detail: 10 points.
- Business context: 10 points.

The score indicates inquiry completeness and apparent readiness for discovery. It is not a probability of conversion and is not trained on historical data.

## 7. Evaluation Plan

Use a human-labelled test set of representative inquiries.

Metrics:
- Field extraction precision, recall and F1.
- Industry classification accuracy.
- Project/service classification accuracy.
- Missing-field detection precision and recall.
- Human rating of follow-up question usefulness.
- Median analysis latency.
- Failure rate and cost per inquiry.

For a future conversion prediction model, collect approved historical lead records with outcomes, define a time-based train/test split, compare a simple logistic regression baseline with tree-based models, calibrate probabilities and monitor drift. Do not train until data volume, quality, consent and label definitions are adequate.

## 8. Security and Responsible AI

- Keep API keys in environment variables.
- Never commit `.env` or customer data.
- Avoid storing inquiries by default.
- Minimize personal and sensitive data.
- Treat inquiry text as untrusted input.
- Require human review before contacting customers or issuing quotes.
- Apply rate limits, authentication and logging controls before public production deployment.

## 9. Execution Plan

**Phase 1 — PoC:** Streamlit UI, FastAPI endpoint, deterministic extraction, optional LLM enrichment and sample cases.

**Phase 2 — Pilot:** Obtain approved anonymized inquiries, define labels with sales stakeholders, evaluate extraction and scoring.

**Phase 3 — Integration:** Connect CRM, add role-based access, audit logs and human feedback.

**Phase 4 — Production:** Deploy securely, monitor latency/cost/errors, review bias and periodically recalibrate rules or models.

## 10. Limitations

- No private Cynbit CRM data was available.
- Sample inquiries are synthetic.
- Budget and timeline extraction uses simple patterns and may miss unusual formats.
- Service classification uses keyword matching in the baseline.
- The score is heuristic, not predictive.
- LLM enrichment quality depends on model availability and output correctness.
- Production readiness requires security, privacy, integration and user acceptance testing.

## 11. Conclusion

The prototype demonstrates an end-to-end technical approach while clearly separating deterministic scoring from optional LLM-assisted extraction. It provides a practical foundation for a measured pilot, rather than claiming unvalidated production performance.


## 12. Context-aware follow-up conversation

After analysis, the customer can ask questions about their project in a chat interface. Each answer receives the original inquiry, generated analysis and recent conversation turns. The system prompt requires evidence-grounded responses, prohibits invented pricing and delivery promises, and asks for clarification when the context is insufficient. Groq is used when configured; a limited deterministic fallback is available without an API key. The prototype stores chat turns only in Streamlit session state and does not persist them.
