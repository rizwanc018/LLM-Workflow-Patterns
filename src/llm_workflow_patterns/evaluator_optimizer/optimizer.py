import logging
from typing import Optional

from llm_workflow_patterns.config.config import MODEL, client
from llm_workflow_patterns.evaluator_optimizer.model import EvaluationFeedBack, SupportResponse

logger = logging.getLogger(__name__)

system_prompt = """
    You are an experienced customer support specialist.

    Write a helpful response to the customer's message.

    Requirements:
    - Be friendly, empathetic, and professional.
    - Address the customer's actual concern.
    - Use clear, concise language.
    - Provide actionable next steps when appropriate.
    - Never invent order details, refunds, policies, or actions
      that have not been confirmed.
    - Do not promise outcomes that are not guaranteed.

    If a previous response and evaluation feedback are provided,
    improve the previous response using that feedback.
    Fix the identified issues while preserving its strengths.
    Do not blindly follow feedback that would require inventing facts.

    Return the result using the SupportResponse schema.
    """


def optimize_response(customer_message: str, previous_response: Optional[str] = None, feedback: Optional[EvaluationFeedBack] = None):
    if previous_response is not None:
        logger.info("Optimizing customer support response")
    else:
        logger.info("Generating customer support response")

    user_prompt = f"""
        Customer message:
        {customer_message}
        """
    if previous_response is not None and feedback is not None:
        user_prompt += f"""

            Previous response:
            {previous_response}

            Evaluator feedback:
            {feedback.model_dump_json(indent=2)}

            Write an improved version of the response.
            """

    result = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=SupportResponse,
    )

    message = result.choices[0].message

    if message.parsed is None:
        raise ValueError(
            f"Optimizer failed. Refusal: {message.refusal}"
        )

    if previous_response is not None:
        logger.info("Response optimized")
    else:
        logger.info("Response generated")

    return message.parsed
