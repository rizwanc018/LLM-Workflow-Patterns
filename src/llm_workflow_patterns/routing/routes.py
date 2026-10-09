import logging

from llm_workflow_patterns.config.config import MODEL,client
from llm_workflow_patterns.routing.models import SupportRequestType, SupportResponse

logger = logging.getLogger(__name__)


def route_support_request(user_input: str) -> SupportRequestType:
    logger.info("Routing user input")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Determine which type of support request the customer is making. Return the request type, your confidence score, and a concise description of the customer's request.",
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        response_format=SupportRequestType
    )

    message = completion.choices[0].message
    if message.parsed is None:
        error_msg = (
            f"Failed to route support request. Refusal: {message.refusal}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = message.parsed
    logger.info(
        f"Support request routed as: {result.request_type} with confidence: {result.confidence_score:.2f}"
    )
    logger.info(f"Description: {result.description}")

    return result


def handle_payment_request(description: str) -> SupportResponse:
    logger.info("Processing payment support request")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Handle the customer's payment-related support request. Provide a clear, helpful, and concise response. "
            },
            {
                "role": "user",
                "content": description
            }
        ],
        response_format=SupportResponse
    )

    message = completion.choices[0].message

    if message.parsed is None:
        error_msg = f"Failed to generate payment support response. Refusal: {message.refusal}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = message.parsed
    logger.info(f"Payment support response generated - Tone: {result.tone}")
    return result


def handle_technical_request(description: str) -> SupportResponse:
    logger.info("Processing technical support request")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Handle the customer's technical support request."
                ),
            },
            {
                "role": "user",
                "content": description,
            },
        ],
        response_format=SupportResponse,
    )

    message = completion.choices[0].message

    if message.parsed is None:
        error_msg = (
            f"Failed to generate technical support response. Refusal: {message.refusal}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = message.parsed
    logger.info(f"Technical support response generated - Tone: {result.tone}")
    return result


def handle_account_request(description: str) -> SupportResponse:
    logger.info("Processing account support request")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Handle the customer's account-related support request. "
                ),
            },
            {
                "role": "user",
                "content": description,
            },
        ],
        response_format=SupportResponse,
    )

    message = completion.choices[0].message

    if message.parsed is None:
        error_msg = (
            f"Failed to generate account support response. Refusal: {message.refusal}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = message.parsed
    logger.info(f"Account support response generated - Tone: {result.tone}")
    return result
