from pydantic import BaseModel, Field


class SupportResponse(BaseModel):
    response: str = Field(description="The response to send to the customer.")


class EvaluationFeedBack(BaseModel):
    score: float = Field(
        ge=0.0, le=1.0, description="Overall quality score from 0.0 to 1.0.")
    passed: bool = Field(
        description="Whether the response meets all quality requirements."
    )
    strengths: list[str] = Field(description="What the response does well.")
    issues: list[str] = Field(
        description="Specific problems that must be corrected.")
    suggestions: list[str] = Field(
        description="Actionable suggestions for improving the response.")
    overall_feedback: str = Field(
        description="A concise explanation of the evaluation."
    )
