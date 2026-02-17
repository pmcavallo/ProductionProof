import anthropic

from prompts.risk_prompt import SYSTEM, USER_TEMPLATE

MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 8192


def generate_risk_assessment(
    project_description: str, client: anthropic.Anthropic | None = None
) -> tuple[str, dict]:
    """Generate a production risk assessment from a project description.

    Returns (text, usage) where usage has input_tokens and output_tokens.
    """
    client = client or anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM,
        messages=[
            {"role": "user", "content": USER_TEMPLATE.format(project_description=project_description)}
        ],
    )
    usage = {"input_tokens": message.usage.input_tokens, "output_tokens": message.usage.output_tokens}
    return message.content[0].text, usage
