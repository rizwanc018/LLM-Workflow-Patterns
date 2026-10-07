from typing import Literal, Optional

from pydantic import BaseModel, Field


class TicketClassification(BaseModel):
    category: Literal["payment", "shipping", "technical", "other"] = Field(
        description="The primary category of the customer's support request.")
    is_support_request: bool = Field(
        description="Whether the user's message is a customer support request that requires assistance or resolution."
    )
    confidence_score: float = Field(
        description="Confidence score between 0 and 1 indicating how confident you are that the selected category and support request classification are correct."
    )


class TicketDetails(BaseModel):
    issue: str = Field(
        description="A concise description of the customer's main problem or issue."
    )
    order_id: Optional[str] = Field(
        description="The customer's order ID if it is explicitly mentioned in the message; otherwise, return null."
    )
    payment_status: Optional[str] = Field(
        description="The payment-related information mentioned by the customer, such as paid, pending, failed, refunded, or unknown. Return null if it is not mentioned"
    )
    urgency: Literal["low", "medium", "high"] = Field(
        description="The urgency of the customer's issue. Use 'high' for issues requiring immediate attention, 'medium' for issues that should be resolved soon, and 'low' for non-urgent issues."
    )

    customer_requested_action: str = Field(
        description="The specific action or resolution the customer is asking the support team to take."
    )


class Resolution(BaseModel):
    recommended_action: str = Field(
        description="The specific action the support team should take to resolve the customer's issue."
    )

    should_escalate: bool = Field(
        description="Whether the ticket should be escalated to a specialized support team or higher-level support."
    )

    department: Literal["billing", "shipping", "technical", "general"]

    reasoning: str = Field(
        description="A brief explanation of why this action, escalation decision, and department were selected based on the ticket details."
    )


class SupportResponse(BaseModel):
    response: str = Field(
        description="The final response to send to the customer."
    )

    tone: Literal["friendly", "professional", "empathetic"] = Field(
        description="The tone used in the customer response."
    )
