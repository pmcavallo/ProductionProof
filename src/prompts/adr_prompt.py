SYSTEM = "You are a senior software architect who writes Architecture Decision Records (ADRs) for enterprise review."

USER_TEMPLATE = """Analyze this project description and generate Architecture Decision Records (ADRs).

PROJECT DESCRIPTION:
{project_description}

Generate a Markdown document containing ADRs extracted from this project. For EACH architectural decision you can identify:

1. Give it a sequential ADR number (ADR-001, ADR-002, etc.)
2. Title: A concise decision statement
3. Status: Accepted
4. Context: Why this decision was needed (infer from the project description)
5. Decision: What was decided and why
6. Consequences: Positive and negative implications
7. Alternatives Considered: What else could have been chosen (with brief rationale for rejection)

Extract REAL decisions from the description — don't invent generic ones. Look for:
- Technology choices (languages, frameworks, databases, APIs)
- Architectural patterns (microservices, monolith, event-driven, multi-agent)
- Data flow decisions
- Integration approaches
- Testing strategies

Format as a single Markdown document with a title header and each ADR as a section.
Output ONLY the Markdown content, no preamble."""
