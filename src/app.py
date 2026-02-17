import os
import tempfile
import time
import traceback
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from generators import generate_adr, generate_risk_assessment, generate_test_coverage

OUTPUT_DIR = Path(tempfile.mkdtemp(prefix="productionproof_"))

# Sonnet 4.5 pricing per million tokens
PRICE_INPUT = 3.00    # $/M input tokens
PRICE_OUTPUT = 15.00  # $/M output tokens


def _write_file(filename: str, content: str) -> str:
    """Write content to a markdown file and return the path."""
    path = OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")
    return str(path)


def generate_all(project_description: str):
    """Generate all three documents from a project description.

    Yields partial results so the UI updates as each document completes.
    """
    no_file = gr.update(value=None, visible=False)
    no_stats = ""

    if not project_description.strip():
        msg = "Please enter a project description."
        yield msg, msg, msg, no_file, no_file, no_file, no_file, no_stats
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        msg = "**Error:** ANTHROPIC_API_KEY not found in environment. Check your .env file."
        yield msg, msg, msg, no_file, no_file, no_file, no_file, no_stats
        return

    import anthropic
    client = anthropic.Anthropic()

    generating = "*Generating... please wait.*"
    queued = "*Queued — waiting for previous step to finish.*"
    adr = generating
    risk = queued
    test_cov = queued
    total_input = 0
    total_output = 0
    start_time = time.time()

    def show_file(path: str) -> dict:
        return gr.update(value=path, visible=True)

    def _cost_summary() -> str:
        elapsed = time.time() - start_time
        cost = (total_input * PRICE_INPUT + total_output * PRICE_OUTPUT) / 1_000_000
        return (
            f"**Generation complete** — {elapsed:.0f}s | "
            f"{total_input + total_output:,} tokens | "
            f"${cost:.4f} (Sonnet 4.5)"
        )

    try:
        yield adr, risk, test_cov, no_file, no_file, no_file, no_file, no_stats

        print("Generating ADR...")
        adr, usage = generate_adr(project_description, client=client)
        total_input += usage["input_tokens"]
        total_output += usage["output_tokens"]
        adr_path = _write_file("architecture_decision_records.md", adr)
        risk = generating
        yield adr, risk, test_cov, show_file(adr_path), no_file, no_file, no_file, no_stats

        print("Generating Risk Assessment...")
        risk, usage = generate_risk_assessment(project_description, client=client)
        total_input += usage["input_tokens"]
        total_output += usage["output_tokens"]
        risk_path = _write_file("risk_assessment.md", risk)
        test_cov = generating
        yield adr, risk, test_cov, show_file(adr_path), show_file(risk_path), no_file, no_file, no_stats

        print("Generating Test Coverage Matrix...")
        test_cov, usage = generate_test_coverage(project_description, client=client)
        total_input += usage["input_tokens"]
        total_output += usage["output_tokens"]
        test_path = _write_file("test_coverage_matrix.md", test_cov)

        combined = (
            f"# ProductionProof Report\n\n---\n\n"
            f"{adr}\n\n---\n\n"
            f"{risk}\n\n---\n\n"
            f"{test_cov}"
        )
        combined_path = _write_file("productionproof_full_report.md", combined)

        yield (adr, risk, test_cov,
               show_file(adr_path), show_file(risk_path),
               show_file(test_path), show_file(combined_path),
               _cost_summary())
        print("Done!")

    except Exception as e:
        error_msg = f"**Error:** {type(e).__name__}: {e}\n\n```\n{traceback.format_exc()}\n```"
        yield error_msg, error_msg, error_msg, no_file, no_file, no_file, no_file, no_stats


def build_ui() -> gr.Blocks:
    """Build and return the Gradio UI."""
    with gr.Blocks(title="ProductionProof") as app:
        gr.Markdown(
            "# ProductionProof\n"
            "Generate production readiness documentation for AI/ML projects.\n"
            "Paste your project description below and click **Generate**.\n"
            "You can read the output in each tab and download the files below."
        )

        project_input = gr.Textbox(
            label="Project Description",
            placeholder="Describe your project: architecture, tech stack, what it does, what's tested, what isn't...",
            lines=10,
        )

        generate_btn = gr.Button("Generate Documentation", variant="primary")

        with gr.Tabs():
            with gr.Tab("Architecture Decision Records"):
                adr_output = gr.Markdown(label="ADR")
                adr_file = gr.File(label="Download ADR", visible=False)

            with gr.Tab("Risk Assessment"):
                risk_output = gr.Markdown(label="Risk Assessment")
                risk_file = gr.File(label="Download Risk Assessment", visible=False)

            with gr.Tab("Test Coverage Matrix"):
                test_output = gr.Markdown(label="Test Coverage Matrix")
                test_file = gr.File(label="Download Test Coverage Matrix", visible=False)

        combined_file = gr.File(label="Download Full Report (all 3 documents)", visible=False)

        stats_output = gr.Markdown()

        generate_btn.click(
            fn=generate_all,
            inputs=[project_input],
            outputs=[adr_output, risk_output, test_output, adr_file, risk_file, test_file, combined_file, stats_output],
        )

    return app


if __name__ == "__main__":
    ui = build_ui()
    ui.queue()  # Required for long-running operations like API calls
    ui.launch()
