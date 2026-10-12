
import logging

from llm_workflow_patterns.config.config import MODEL, client
from llm_workflow_patterns.orchestrator_workers.model import ResearchReport, ReviewFeedback

logger = logging.getLogger(__name__)

system_prompt = """
    You are a critical research report reviewer.

    Evaluate the supplied report for accuracy, completeness, and coherence.

    Review criteria:

    1. Accuracy:
       - Are the conclusions supported by the information provided?
       - Are unsupported claims, assumptions, or overgeneralizations present?
       - Does the report acknowledge uncertainty and evidence gaps?

    2. Completeness:
       - Does the report address the research topic thoroughly?
       - Are important perspectives or questions missing?
       - Are the recommendations relevant to the findings?

    3. Coherence:
       - Is the report logically organized?
       - Are the findings consistent with the analysis and recommendations?
       - Are there contradictions or unnecessary repetitions?

    Instructions:
    - Give each score a value between 0.0 and 1.0.
    - Be critical and specific rather than automatically approving the report.
    - Explain missing information and recommend concrete improvements.
    - Do not invent facts or sources to justify your review.
    - Do not claim that facts have been independently verified.
    - Evaluate the report as supplied; do not rewrite the entire report.

    Return your evaluation using the ReviewFeedback schema.
    """


def review_report(report: ResearchReport) -> ReviewFeedback:
    logger.info("Reviewing research report: %s", report.title)


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
                Review the following research report:

                {report.model_dump_json(indent=2)}

                Evaluate its accuracy, completeness, and coherence.
                Provide specific feedback and actionable improvements.
                """,
            },
        ],
        response_format=ReviewFeedback,
    )

    message = response.choices[0].message

    if message.parsed is None:
        raise ValueError(
            "Failed to review research report. "
            f"Refusal: {message.refusal}"
        )

    feedback = message.parsed

    logger.info(
        "Report review completed. Accuracy: %.2f, "
        "Completeness: %.2f, Coherence: %.2f",
        feedback.accuracy_score,
        feedback.completeness_score,
        feedback.coherence_score,
    )

    return feedback
