import logging

from llm_workflow_patterns.config.config import MODEL,client
from llm_workflow_patterns.orchestrator_workers.model import ResearchFinding, ResearchReport

logger = logging.getLogger(__name__)

system_prompt = """
    You are a research report synthesizer.

    Your job is to combine findings from multiple research workers into
    one clear, coherent, evidence-aware research report.

    Instructions:
    1. Address the original research question directly.
    2. Combine related findings and remove unnecessary repetition.
    3. Identify agreements, disagreements, and connections between findings.
    4. Distinguish supported conclusions from assumptions or uncertainties.
    5. Use the evidence and limitations provided by the workers.
    6. Do not invent facts, statistics, sources, or citations.
    7. Do not claim that evidence has been verified if it has not.
    8. Include actionable recommendations that follow from the findings.
    9. Preserve important limitations and conflicting information.
    10. Do not simply copy each worker's findings into separate sections.

    Produce a useful, self-contained research report.

    Return the result using the ResearchReport schema.
    """


def synthesize_report(topic: str, findings: list[ResearchFinding]) -> ResearchReport:
    logger.info(
        "Synthesizing research report from %d findings",
        len(findings),
    )

    if not findings:
        raise ValueError("Cannot synthesize a report without findings.")

    findings_json = "\n".join(
        finding.model_dump_json(indent=2) for finding in findings
    )

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"""
                Research Question:
                {topic}

                Research Findings:
                {findings_json}

                Synthesize these findings into a comprehensive report
                that answers the original research question.
                """,
            },
        ],
        response_format=ResearchReport,
    )

    message = response.choices[0].message

    if message.parsed is None:
        raise ValueError(
            "Failed to synthesize research report. "
            f"Refusal: {message.refusal}"
        )

    result = message.parsed

    logger.info("Research report synthesized: %s", result.title)

    return result
