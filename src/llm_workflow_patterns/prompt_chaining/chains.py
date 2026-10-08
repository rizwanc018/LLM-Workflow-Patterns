import logging

from llm_workflow_patterns.prompt_chaining.config import client, MODEL
from llm_workflow_patterns.prompt_chaining.models import TicketClassification, TicketDetails, Resolution, SupportResponse

logger = logging.getLogger(__name__)


def classify_ticket(user_input: str) -> TicketClassification:
    logger.info("Starting ticket classification")
    logger.debug(f"Input text: {user_input}")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Analyze whether this text is a customer support request.",
            },
            {"role": "user", "content": user_input},
        ],
        response_format=TicketClassification
    )

    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Failed to parse ticket classification")

    logger.info(
        f"Classification complete - Category: {result.category}, Is customer support request: {result.is_support_request}, Cofidence score: {result.confidence_score}")
    return result


def parse_ticket_details(user_input: str) -> TicketDetails:
    logger.info("Starting details parsing")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Analyze the customer's support request and extract the relevant ticket details.",
            },
            {"role": "user", "content": user_input},
        ],
        response_format=TicketDetails
    )

    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Failed to parse ticket details")

    logger.info(
        f"Details parsing complete- issues: {result.issue}, Order Id: {result.order_id}, Payemnt staus: {result.payment_status}, Urgency: {result.urgency}, Requested action : {result.customer_requested_action},")
    return result


def resolve_ticket(ticket_details: TicketDetails) -> Resolution:
    logger.info("Starting ticket resolution")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Analyze the customer support ticket details and determine the appropriate resolution.",
            },
            {
                "role": "user",
                "content": str(ticket_details.model_dump()),
            },
        ],
        response_format=Resolution,
    )

    result = completion.choices[0].message.parsed

    if result is None:
        raise ValueError("Failed to parse ticket resolution")

    logger.info(
        f"Resolution complete - Action: {result.recommended_action}, Escalate: {result.should_escalate}, Department: {result.department}"
    )

    return result


def generate_support_response(
    ticket_details: TicketDetails,
    resolution: Resolution,
) -> SupportResponse:
    logger.info("Generating support response")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Generate a customer-facing response based on the ticket details and the recommended resolution.",
            },
            {
                "role": "user",
                "content": f"""
                            Ticket Details:
                            {ticket_details.model_dump()}

                            Resolution:
                            {resolution.model_dump()}
                            """,
            },
        ],
        response_format=SupportResponse,
    )

    result = completion.choices[0].message.parsed

    if result is None:
        raise ValueError("Failed to generate support response")

    logger.info(
        f"Support response generated successfully - Tone: {result.tone}"
    )

    return result
