# ProductionProof

Generate production readiness documentation for AI/ML projects. Turns a project description into three enterprise-grade artifacts:

- **Architecture Decision Records (ADRs)** — extracted architectural decisions with context, consequences, and alternatives
- **Risk Assessment** — categorized risk register with severity, likelihood, mitigations, and identified gaps
- **Test Coverage Matrix** — component-level coverage status with critical gaps and recommended test plan

## Setup

```bash
# Create virtual environment
py -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
copy .env.example .env
# Edit .env and add your Anthropic API key
```

## Usage

```bash
py -m src.app
```

Open the Gradio UI (default: http://localhost:7860), paste your project description, and click **Generate Documentation**.

## Example Input

See `examples/sample_input.txt` for a sample project description.

## Project Structure

```
src/
├── app.py              # Gradio UI
├── generators/         # Document generators (one per artifact)
│   ├── adr.py
│   ├── risk.py
│   └── test_coverage.py
└── prompts/            # Structured prompts for each generator
    ├── adr_prompt.py
    ├── risk_prompt.py
    └── test_coverage_prompt.py
```
