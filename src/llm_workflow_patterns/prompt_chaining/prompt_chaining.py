import logging

from .chains import classify_ticket, parse_ticket_details, resolve_ticket, generate_support_response
from .models import SupportResponse

logger = logging.getLogger(__name__)


def process_support_ticket(user_input: str) -> SupportResponse | None:
    logging.info("Processing user input")

    ticket_classification = classify_ticket(user_input)
    if not ticket_classification:
        logger.warning("Classification check failed - NO RESULT")
        return None

    if (not ticket_classification.is_support_request or ticket_classification.confidence_score < 0.7):
        logger.warning(
            f"Gate check failed - is_support_request: {ticket_classification.is_support_request}, confidence: {ticket_classification.confidence_score:.2f}")
        return None

    logger.info("Gate check passed, Proceeding to ticket details processing.")

    ticket_details = parse_ticket_details(user_input)
    logger.info("Ticket details processed, Proceeding to ticket resolution.")

    resolution = resolve_ticket(ticket_details)
    if resolution.should_escalate:
        logger.info(
            f"Ticket requires human escalation - Department: {resolution.department}"
        )
        print(
            f"⚠️ This ticket requires human assistance. "
            f"Escalating to the {resolution.department} team."
        )
        return None

    logger.info(
        "Ticket does not require escalation, generating support response.")

    support_response = generate_support_response(ticket_details, resolution)
    logger.info(f"Support response generated successfully")

    return support_response
