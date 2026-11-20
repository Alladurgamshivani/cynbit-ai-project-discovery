# AI Opportunity Report

**Identifying practical AI/ML opportunities for Cynbit**  
**Cynbit AI/ML Engineer Intern Technical Assessment**

## 1. Purpose

The purpose of this report is to identify practical areas where AI and machine learning could support Cynbit's services, products and internal work. The assessment brief asks for an industry analysis, a set of possible opportunities and one opportunity that can be demonstrated through a working proof of concept.

The opportunity selected for this project is an AI-powered project discovery and lead qualification assistant. It is intended to help a team make sense of incoming project enquiries before the first detailed discussion with a prospective customer.

## 2. Understanding the business

Cynbit's public-facing business information describes technology services and software products. The areas relevant to this assessment include AI automation, custom software development and SaaS products. The product names discussed in the research and project notes include Cynbit Studio, Revio and TenantEase.

These products suggest several possible areas for AI support:

- Career and learning services can use personalization and skill-gap analysis.
- Reputation management services can use sentiment and complaint analysis.
- Property management services can use payment-pattern analysis and workflow assistance.
- Software and AI service enquiries can use automated requirement capture and project discovery.

This is an external assessment based on publicly available information. It does not assume access to Cynbit's internal customer records, sales processes or operational metrics. The opportunities below should therefore be treated as proposals for investigation, not as confirmed problems within the company.

## 3. Industry context

Software service providers receive enquiries in different formats and with different levels of detail. Some customers know exactly what they want to build. Others describe a business problem without knowing which technology or service would address it.

A project enquiry may mention a business goal, a few desired features, a budget and a preferred launch date. Important details such as existing systems, user roles, security needs, integrations and ongoing support may be missing.

AI can help organize this information. Natural-language processing and large language models can extract details from free-text messages, classify the type of request and prepare follow-up questions. Rule-based checks can then identify incomplete information. A human team member should review the result before making commitments to a customer.

Other relevant uses of AI in this industry include customer support automation, document processing, internal knowledge search, predictive analytics and personalized recommendations.

## 4. Opportunities identified

### 4.1 Project discovery and lead qualification

A customer enquiry can be processed into a structured record containing the industry, project type, requested features, budget, timeline and integrations. The system can point out missing details, suggest a suitable service category and prepare questions for the next discussion.

**Potential value:**

- Less time spent reading and organizing unstructured enquiries.
- More consistent initial requirement capture.
- Earlier identification of missing project information.
- A clearer starting point for a discovery call.

### 4.2 Reputation intelligence for Revio

A reputation management product could use sentiment analysis and topic classification to group reviews by issue, such as delivery, product quality or customer service. It could identify recurring complaints and highlight changes in customer feedback.

**Potential value:**

- Easier review analysis across multiple sources.
- Faster identification of recurring customer concerns.
- Better information for businesses preparing responses.

### 4.3 Personalized learning support for Cynbit Studio

A learning platform could analyze assessment results and learning activity to identify areas where a learner needs more practice. It could recommend lessons or exercises based on demonstrated gaps rather than showing the same learning path to everyone.

**Potential value:**

- More relevant learning recommendations.
- Clearer visibility into skill gaps.
- A more adaptive learning experience.

### 4.4 Payment-pattern analysis for TenantEase

A property management platform could summarize historical payment patterns and flag accounts that may need a reminder or manual follow-up. Any risk indicator should be used to support a property manager, not to make an automatic decision against a tenant.

**Potential value:**

- Better organization of payment follow-ups.
- Earlier visibility of delayed-payment patterns.
- Less manual review of payment histories.

### 4.5 Internal knowledge assistant

An internal assistant could search approved company documents, project notes and technical documentation. Retrieval-augmented generation (RAG) could provide answers with references to the source documents.

**Potential value:**

- Faster access to internal information.
- Less repeated searching across documents.
- More consistent answers to common internal questions.

## 5. Comparing the opportunities

The table below is an initial assessment by the candidate. The ratings are qualitative estimates for this assignment, not measured business results.

| Opportunity | Business relevance (1-5) | Feasibility for a small PoC (1-5) | Demo potential (1-5) |
|---|---:|---:|---:|
| Project discovery assistant | 5 | 5 | 5 |
| Reputation intelligence | 5 | 3 | 4 |
| Learning recommendations | 4 | 4 | 4 |
| Payment-pattern analysis | 4 | 3 | 4 |
| Internal knowledge assistant | 4 | 4 | 4 |

The project discovery assistant is the best fit for this assessment because it relates to software and AI service enquiries and can be demonstrated without using private customer information. It also has a clear workflow that can be tested with sample enquiries.

## 6. Selected opportunity: AI project discovery assistant

The proposed application accepts a customer enquiry written in ordinary language. It then prepares a structured summary for review by a sales or project team member.

The proof of concept is designed to:

1. Identify the likely industry and project type.
2. Extract requirements mentioned by the customer.
3. Identify a budget and timeline when these are stated.
4. Detect integration references.
5. List information that appears to be missing.
6. Recommend a relevant service category.
7. Generate follow-up questions.
8. Produce a short project discovery brief.
9. Provide a rule-based inquiry-readiness score with an explanation of the factors used.

**Example enquiry:**

> "We are a healthcare company looking for a multilingual AI chatbot for our website. It should answer common patient questions and integrate with our existing website. Our budget is around INR 200000 and we hope to launch in two months."

An expected structured summary would identify healthcare as the industry, an AI chatbot as the project type, multilingual support and website integration as requirements, INR 200000 as the stated budget and two months as the stated target. The system should also ask about the information sources the chatbot can use, the process for escalating questions to staff, security requirements and expected usage.

The system must distinguish information supplied by the customer from suggestions generated by the assistant. It should not treat an unconfirmed suggestion as an agreed requirement.

## 7. How the priority score works

The current proof of concept uses a transparent rule-based score. It does not use a trained model to predict whether a lead will convert.

The illustrative score assigns:

- Up to 20 points for a clearly stated business need.
- Up to 20 points when a budget is provided.
- Up to 15 points when a timeline is provided.
- Up to 25 points for the amount of requirement detail detected.
- Up to 10 points for integration or delivery details.
- Up to 10 points for business context.

The score is capped at 100. The current priority bands are High for 70-100, Medium for 40-69 and Low for 0-39. These weights and bands are initial design choices. They would need to be reviewed with the business team before being used in a real sales process.

The score indicates how complete an enquiry appears under these rules. It is not a conversion probability, a measure of customer value or a recommendation to reject a customer.

## 8. Expected benefits and how to evaluate them

The proposed system may reduce the amount of manual work needed to organize enquiries and prepare for an initial discussion. This benefit should be tested rather than assumed.

A pilot could use a set of approved, anonymized enquiries. Team members would label the industry, project type, key requirements and missing fields. The system's output could then be compared with those labels.

Useful evaluation measures include:

- Precision, recall and F1 for extracted fields.
- Accuracy for industry and service classification.
- Precision and recall for missing-information detection.
- Human review of the usefulness of follow-up questions.
- Time taken to prepare a discovery summary.
- Response latency, error rate and cost per enquiry.

No accuracy or time-saving result is claimed in this report because a representative Cynbit dataset was not available for evaluation.

## 9. Risks and safeguards

**Incorrect extraction:** The assistant may misunderstand a customer's wording. Important fields should be reviewed by a person.

**Unsupported claims:** The assistant must not invent prices, delivery dates, integrations or service commitments. If information is missing, it should say so and ask for clarification.

**Customer privacy:** Real enquiries may contain personal or confidential information. A pilot should use approved data, limit retention and avoid collecting information that is not needed.

**Prompt injection:** Customer messages should be treated as input data, not instructions that can change the assistant's role or safety rules.

**Unfair prioritization:** The score should be explainable, reviewed regularly and open to human override. It should not be used as the only basis for deciding whether to engage with a customer.

## 10. Conclusion

The project discovery assistant is a practical opportunity to demonstrate AI in a software services workflow. It brings together text understanding, structured extraction, simple decision rules and conversational follow-up.

The current prototype is a starting point. Before wider use, it would need testing on representative enquiries, review by the relevant business team and appropriate security and privacy controls. A later version could connect to a CRM and use human feedback to improve extraction and workflow design.
