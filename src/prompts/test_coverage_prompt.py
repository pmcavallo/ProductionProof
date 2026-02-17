SYSTEM = "You are a QA engineering lead who assesses test coverage for production readiness reviews."

USER_TEMPLATE = """Analyze this project description and generate a Test Coverage Matrix.

PROJECT DESCRIPTION:
{project_description}

Generate a Markdown document with:

## 1. Coverage Summary
High-level assessment: what percentage of critical paths appear tested vs. untested based on the description.

## 2. Test Coverage Matrix
A table with columns: Component | Test Type | Coverage Status (Tested/Partial/Untested/Unknown) | Evidence | Risk if Untested

Test types to assess for each component:
- Unit tests
- Integration tests
- End-to-end tests
- Performance/load tests
- Security tests
- Edge case tests
- Failure/recovery tests

## 3. Critical Gaps
Components or scenarios that are explicitly untested or where testing status is unknown, ranked by production risk.

## 4. Recommended Test Plan
Specific tests that should be added before production deployment, prioritized by risk.

Base your assessment ONLY on what the description states or implies. If testing isn't mentioned for a component, mark it as "Unknown" not "Untested". If the description says something IS tested, note the evidence. If it says something is NOT tested, flag it as a critical gap.

Output ONLY the Markdown content, no preamble."""
