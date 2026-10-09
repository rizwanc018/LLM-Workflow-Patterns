from typing import Literal

from pydantic import BaseModel, Field

class SupportRequestType(BaseModel):
    request_type: Literal[
        "payment",
        "technical",
        "account",
        "general"
    ] = Field(description="The type of customer support request.")
    confidence_score: float = Field(
        description="Confidence score between 0 and 1 for the classification.")
    description: str = Field(
        description="A concise description of the customer's request."
    )


class SupportResponse(BaseModel):
    response: str = Field(description="The response to send to customer.")
    tone: Literal["friendly", "professional", "empathetic"] = Field(
        description="The tone of the response."
    )
