import logging

from llm_workflow_patterns.evaluator_optimizer.evaluator import evaluate_response
from llm_workflow_patterns.evaluator_optimizer.optimizer import optimize_response


logger = logging.getLogger(__name__)


def improve_support_response(customer_message: str, max_iterations: int = 3) -> str:
    if max_iterations < 1:
        raise ValueError("Max iteration must be at least 1.")

    previous_response = None
    feedback = None

    for iteration in range(1, max_iterations + 1):
        logger.info(
            "Generating response: iteration %d",
            iteration,
        )

        response = optimize_response(
            customer_message=customer_message,
            previous_response=previous_response,
            feedback=feedback,
        )

        feedback = evaluate_response(
            customer_message=customer_message,
            response=response.response,
        )

        logger.info(
            "Evaluation score: %.1f | Passed: %s", feedback.score, feedback.passed)

        if feedback.passed:
            logger.info("Response passed evaluation.")
            return response.response

        previous_response = response.response

        logger.info("Improvements needed: %s", feedback.issues)

    logger.warning(
        "Maximum iterations reached. Returning the last candidate."
    )

    assert previous_response is not None
    return previous_response


def main():
    customer_message = (
        "My payment was deducted, but my order is still pending. "
        "I have been waiting for two hours. Please help."
    )

    final_response = improve_support_response(customer_message)
    print("\nFinal response:\n")
    print(final_response)


if __name__ == "__main__":
    main()
