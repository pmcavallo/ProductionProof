SYSTEM = "You are a production risk analyst specializing in AI/ML systems for regulated industries."

USER_TEMPLATE = """Analyze this project description and generate a Production Risk Assessment.

PROJECT DESCRIPTION:
{project_description}

Generate a Markdown risk assessment document with:

## 1. Executive Summary
Brief overview of the system and its risk profile.

## 2. Risk Register
A table with columns: Risk ID | Description | Category | Severity (Critical/High/Medium/Low) | Likelihood (High/Medium/Low) | Impact | Mitigation Strategy | Status

Categories to consider:
- **Data risks**: Quality, availability, drift, bias, privacy
- **Model risks**: Accuracy degradation, hallucination, adversarial inputs
- **Infrastructure risks**: Scalability, latency, single points of failure
- **Operational risks**: Monitoring gaps, incident response, rollback capability
- **Compliance risks**: Regulatory requirements, audit trail, explainability
- **Integration risks**: API dependencies, version compatibility, vendor lock-in

## 3. Identified Gaps
What the project description explicitly or implicitly reveals as untested, unaddressed, or missing.

## 4. Recommendations
Prioritized list of actions to improve production readiness.

Extract CONCRETE risks from the description. If the description mentions something is untested, that's a real gap. If it uses a specific vendor, that's a real lock-in risk.

Output ONLY the Markdown content, no preamble."""
