# Technical Approach Report

**AI-Powered Project Discovery and Lead Qualification Assistant**  
**Cynbit AI/ML Engineer Intern Technical Assessment**

## 1. Objective

This report describes the design and implementation approach for the AI Project Discovery and Lead Qualification Assistant. The application accepts a customer project enquiry and produces a structured summary, identifies missing information, recommends a service category and prepares follow-up questions.

The proof of concept also includes a follow-up chat feature. After the initial analysis, a customer can ask additional questions about the same project. The assistant uses the original enquiry and the generated analysis as context.

## 2. System overview

The application has a Streamlit user interface, Python analysis logic and a FastAPI endpoint. The analysis logic first creates a deterministic baseline result. If a Groq API key is configured, an LLM can enrich selected fields and produce a more natural project brief. The lead-priority score remains rule-based.

The main flow is:

1. Customer enquiry
2. Streamlit interface
3. Input validation
4. Requirement extraction and classification
5. Optional Groq LLM enrichment
6. Rule-based priority score
7. Missing-information and follow-up question generation
8. Project discovery brief
9. Results shown to the user

For the follow-up conversation, the application passes the original enquiry, analysis result and recent conversation turns to the conversation function. The response is shown in the same project session.

## 3. Technology choices

- **Python** is used for the main application logic because it supports rapid development and has libraries for APIs, data validation and language-model integration.
- **Streamlit** provides the user interface. It was selected because it allows the proof of concept to be demonstrated without building a separate frontend application.
- **FastAPI** provides an API endpoint for analysis and a separate endpoint for follow-up questions. This keeps the processing logic accessible to other applications if the prototype is extended later.
- **Pydantic** validates incoming API data and helps keep request structures consistent.
- **Groq** is used as an optional hosted LLM provider. It can help interpret varied customer language and produce structured or conversational responses. The application also has a deterministic fallback so that basic functionality can be demonstrated without an API key.
- **Regular expressions and keyword rules** are used for baseline extraction of budget, timeline, industry, requirements and service category. These rules are simple and transparent, but they will not handle every possible way a customer can express a requirement.
- **Pytest** is used for basic automated tests of the analysis logic.

## 4. Data pipeline

The analysis pipeline follows these steps:

**Step 1: Receive the enquiry.** The customer enters a project description in the Streamlit interface or sends it to the API.

**Step 2: Validate the input.** The application checks that the enquiry is present and meets the configured length limits.

**Step 3: Extract information.** The baseline logic looks for industry terms, project indicators, budget patterns, timeline expressions, requirements and integration references.

**Step 4: Classify the request.** The application selects a likely project or service category based on the terms found in the enquiry.

**Step 5: Identify missing information.** The application checks whether key details such as budget, timeline, industry and integration needs have been provided.

**Step 6: Calculate the score.** The rule-based scoring function assigns points according to the criteria described in this report.

**Step 7: Prepare the response.** The application creates follow-up questions and a project discovery brief and returns the result as structured data.

**Step 8: Continue the conversation.** The customer can ask a follow-up question. The assistant receives the original enquiry and analysis so that it can answer in the context of that project.

The sample enquiries included in the repository are synthetic examples. They are not Cynbit customer records.

## 5. Model and extraction approach

The proof of concept uses a hybrid approach rather than relying entirely on a language model.

The deterministic baseline handles straightforward patterns such as common budget formats, timeline expressions and known requirement keywords. It is useful for repeatable behavior and provides a fallback when the external model is unavailable.

The optional Groq LLM enrichment is intended for cases where natural language is less predictable. The prompt asks the model to identify project type, industry, requirements, follow-up questions and a project brief. It also instructs the model not to invent facts that are absent from the enquiry.

The follow-up assistant uses the original enquiry, structured analysis and recent conversation history. Its instructions require it to distinguish confirmed details from suggestions. If the answer is not supported by the context, it should say that the project team needs to confirm it.

The current system does not train a new machine-learning model. It also does not predict the probability that a lead will become a customer. The priority score is calculated using explicit rules.

## 6. Prompt design

The prompt is designed around a few requirements:

- The assistant acts as a project discovery assistant.
- Customer text is treated as untrusted input data.
- Only details stated or reasonably supported by the enquiry should be extracted.
- Missing budget, timeline or integration information should remain marked as missing.
- Recommendations must be separated from facts supplied by the customer.
- The output should be concise and useful to a project or sales team.
- The assistant must not promise a price, delivery date or technical capability without confirmation.

For the follow-up chat, the prompt includes the original enquiry and analysis result. Recent messages are included to maintain conversational continuity. The assistant is instructed to ask for clarification when the context does not contain enough information to answer.

The LLM output should be checked before it is used in a business workflow. In a production version, a formal response schema, validation and retry handling should be added around model output.

## 7. Lead-priority scoring

The current scoring method is rule-based and uses a maximum of 100 points.

| Criterion | Maximum points |
|---|---:|
| Clear business need | 20 |
| Budget provided | 20 |
| Timeline provided | 15 |
| Requirements clarity | 25 |
| Integration or delivery detail | 10 |
| Business context | 10 |
| **Total** | **100** |

The current bands are High (70-100), Medium (40-69) and Low (0-39). The score is an indication of enquiry completeness under the selected rules. It is not a probability of conversion.

The weights are illustrative and have not been calibrated using Cynbit's historical sales data. They should be reviewed with the business team and changed if the pilot shows that they do not help staff prioritize work.

## 8. Evaluation plan

The initial tests check that the analysis function returns expected fields for sample enquiries, identifies missing information and rejects very short input. These tests check basic functionality; they do not establish model accuracy.

A more complete evaluation should use a representative set of enquiries that has been approved for testing and anonymized where necessary. Human reviewers should label the correct industry, project type, budget, timeline, requirements and missing details.

The following measures can then be calculated:

- Precision, recall and F1 for extracted fields.
- Accuracy for industry and service classification.
- Precision and recall for missing-information detection.
- Human ratings for the relevance of follow-up questions.
- Average and median response time.
- Error rate and cost per enquiry.

The evaluation should include different writing styles, short enquiries, incomplete enquiries, spelling mistakes and requests that do not fit the service categories.

## 9. Security and responsible use

API credentials should be stored in environment variables or a deployment secret manager. They must not be committed to GitHub.

The prototype does not need to store customer enquiries in a database. For a pilot, data collection and retention should be agreed with the company first. Personal and confidential details should be minimized or removed from test data.

Customer input must not be allowed to override the assistant's system instructions. The assistant should not send messages, make quotations or commit to delivery dates without human approval.

Before production use, the API should have authentication, rate limiting, appropriate logging, access controls and monitoring. Error messages should not expose credentials or private customer information.

## 10. Execution plan

**Phase 1 - Proof of concept:**  
Build the Streamlit interface, analysis logic, FastAPI endpoints, sample enquiries, optional LLM enrichment and follow-up chat. Confirm that the main user flow works locally.

**Phase 2 - Evaluation:**  
Prepare an approved and anonymized test set. Ask reviewers to label expected outputs. Measure extraction and classification quality and review the usefulness of the generated questions.

**Phase 3 - Pilot integration:**  
Discuss the workflow with relevant Cynbit team members. If appropriate, connect the application to a CRM using approved APIs. Add human review and feedback capture.

**Phase 4 - Production preparation:**  
Add authentication, rate limits, monitoring, error handling, data retention controls and deployment configuration. Reassess scoring rules and model behavior using pilot feedback.

## 11. Current limitations

- The prototype has not been evaluated on Cynbit's private customer enquiries.
- Sample data is synthetic.
- Keyword and regular-expression extraction can miss unusual wording and formats.
- LLM responses depend on provider availability and model behavior.
- The score is heuristic and is not trained on conversion outcomes.
- The follow-up assistant may need human clarification when project information is incomplete.
- The current application is a proof of concept, not a production-ready sales system.

## 12. Conclusion

The prototype demonstrates how an AI-assisted workflow can organize a customer enquiry, highlight missing project details and support follow-up questions using the same project context.

The hybrid design keeps basic extraction and scoring transparent while allowing an LLM to handle more flexible language.

The next step is to evaluate the system on an approved dataset and review the workflow with business users before considering CRM integration or production deployment.
