import logging

from llm_workflow_patterns.routing.models import SupportResponse
from llm_workflow_patterns.routing.routes import handle_account_request, handle_payment_request, handle_technical_request, route_support_request

logger = logging.getLogger(__name__)


def process_support_request(user_input: str) -> SupportResponse | None:
    classification = route_support_request(user_input)

    if classification.confidence_score < 0.7:
        logger.warning(
            f"Low routing confidence: {classification.confidence_score:.2f}"
        )
        return None

    if (classification.request_type == "payment"):
        response = handle_payment_request(classification.description)
        return response

    if (classification.request_type == "technical"):
        response = handle_technical_request(classification.description)
        return response

    if (classification.request_type == "account"):
        response = handle_account_request(classification.description)
        return response

    else:
        logger.info(
            f"Support request routed as: {classification.request_type} with confidence: {classification.confidence_score:.2f}"
        )
        logger.info(f"Description: {classification.description}")
        return None





def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # user_input = "I want to request a refund for my recent payment."
    # user_input = "The dashboard is loading forever and never shows my data."
    user_input = "My account has been locked. How can I unlock it?"
    # user_input = "Explain how Bitcoin works."
    response = process_support_request(user_input)
    if response:
        print(f"[{response.tone}] {response.response}")


if __name__ == "__main__":
    main()
