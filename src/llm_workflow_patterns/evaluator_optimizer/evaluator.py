
import logging

from openai import OpenAI

from llm_workflow_patterns.config.config import MODEL, client
from llm_workflow_patterns.evaluator_optimizer.model import EvaluationFeedBack

logger = logging.getLogger(__name__)


system_prompt = """
    You are a strict quality evaluator for customer support responses.

    Evaluate the response using these criteria:

    1. Relevance: Does it address the customer's actual concern?
    2. Accuracy: Does it avoid unsupported claims and promises?
    3. Empathy: Does it acknowledge the customer's situation?
    4. Clarity: Is it easy to understand?
    5. Actionability: Does it provide useful next steps when needed?

    Scoring:
    - 0.90 to 1.00: Excellent; ready to use.
    - 0.75 to 0.89: Good, but improvements are needed.
    - Below 0.75: Significant problems remain.

    Set passed=true only when:
    - The score is at least 0.90.
    - There are no critical accuracy or safety issues.
    - The response satisfies the quality criteria.

    Be specific about issues and suggest actionable improvements.
    Do not invent facts when evaluating the response.

    Return the result using the EvaluationFeedback schema.
    """


def evaluate_response(
    customer_message: str,
    response: str,
) -> EvaluationFeedBack:
    logger.info("Evaluating customer support message.")

    result = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
                Customer message:
                {customer_message}

                Candidate response:
                {response}

                Evaluate this response.
                """,
            },
        ],
        response_format=EvaluationFeedBack,
    )

    message = result.choices[0].message

    if message.parsed is None:
        raise ValueError(
            f"Evaluator failed. Refusal: {message.refusal}"
        )

    logger.info("Evaluation complete")

    return message.parsed
