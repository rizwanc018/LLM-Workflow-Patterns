from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    task_name: str = Field(
        description="A short descriptive name for research task.")
    research_question: str = Field(
        description="The specific question the researcher must investigate.")
    objective: str = Field(
        description="What the worker should accomplish through this research task")
    expected_output: str = Field(
        description="The expected output or findings the worker should produce.")


class ResearchPlan(BaseModel):
    topic_analysis: str = Field(
        description="An analysis of the main research question and its scope.")
    research_objective: str = Field(
        description="The overall goal the research report should achive.")
    research_tasks: list[ResearchTask] = Field(
        description="A list of independend task assigned to specialized workers.")


class ResearchFinding(BaseModel):
    task_name: str = Field(
        description="The name of the research task completed by worker.")
    findings: str = Field(
        description="The key findings discovered during the research task.")
    evidence: str = Field(
        description="Supporting eveidences, such as source references, observed data or concrete examples. Do not invent citations.")
    limitations: list[str] = Field(
        description="Knowledge gaps, uncertainties, assumptions, or affecting the findings.")


class ResearchReport(BaseModel):
    title: str = Field(
        description="A concise, informative title for the research report.")
    executive_summary: str = Field(
        description="A summary of main findings, conclusion and recommendations.")
    main_findings: list[str] = Field(
        description="The most important conclusions synthesized from the workers' findings."
    )
    analysis: str = Field(
        description="A detailed analysis comparing the findings and explaining their implications."
    )
    recommendations: list[str] = Field(
        description="Actionable recommendations based on the available evidence."
    )


class ReviewFeedback(BaseModel):
    accuracy_score: float = Field(
        description="Score from 0.0 to 1.0 representing how well the report is supported by the supplied evidence."
    )
    completeness_score: float = Field(
        description="Score from 0.0 to 1.0 representing how thoroughly the report addresses the research objective."
    )
    coherence_score: float = Field(
        description="Score from 0.0 to 1.0 representing the logical flow and consistency of the report."
    )
    missing_information: list[str] = Field(
        description="Important questions, perspectives, or evidence missing from the report."
    )
    suggested_improvements: list[str] = Field(
        description="Specific changes that would improve the report's accuracy, completeness, or clarity."
    )
    overall_feedback: str = Field(
        description="An overall assessment of the report's strengths and weaknesses."
    )
