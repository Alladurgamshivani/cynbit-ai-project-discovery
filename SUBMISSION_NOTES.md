# Candidate submission notes

## Primary deliverable
Paste the public GitHub repository URL after pushing this project.

## Additional deliverables
1. Live Streamlit demo URL (only after deployment and testing).
2. Optional short demo video URL.
3. Optional PDF exports of the two reports.

## Suggested execution notes for the portal

"I developed an AI Project Discovery and Lead Qualification Assistant as a proof of concept. It accepts natural-language project inquiries and extracts industry, project type, budget, timeline, requirements and integrations. It identifies missing information, generates follow-up questions, recommends a relevant service and produces an explainable rule-based priority score. The project includes a Streamlit interface, FastAPI endpoint, optional Groq-based LLM enrichment, deterministic fallback, sample synthetic inquiries, tests, an AI Opportunity Report and a Technical Approach Report. The score is a heuristic readiness indicator and is not presented as a trained conversion probability. Setup and execution instructions are included in the README."

## Before submitting

- [ ] Install dependencies and run the app locally.
- [ ] Run `pytest -q` and record the actual result.
- [ ] Test all three sample inquiries.
- [ ] Check API `/health` and `/docs`.
- [ ] Add screenshots to the repository.
- [ ] Push source code and reports to a public GitHub repository.
- [ ] Verify the repository opens in an incognito/private browser.
- [ ] Deploy only if the live demo has been tested.
- [ ] Paste the primary GitHub URL in the candidate portal.
- [ ] Verify the actual deadline and time zone with the recruiter.


## Follow-up conversation demo
After running a project analysis, scroll to "Ask about your project" and ask a question such as:
- "Can this integrate with our existing website?"
- "What details are still missing?"
- "Is the budget confirmed?"
For open-ended contextual responses, configure `GROQ_API_KEY` in `.env` before launching Streamlit.
