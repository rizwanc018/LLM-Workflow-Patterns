import logging

from llm_workflow_patterns.config.config import MODEL
from llm_workflow_patterns.orchestrator_workers.model import ResearchFinding, ResearchTask
from llm_workflow_patterns.parallelization.validators import asyncClient

logger = logging.getLogger(__name__)

system_prompt = """
    You are a research worker responsible for investigating one specific
    research task within a larger research project.

    Your job is to produce accurate, focused findings that help answer
    the overall research question.

    Instructions:
    1. Focus on the research question and objective provided in the task.
    2. Investigate the task thoroughly using your available knowledge.
    3. Return clear, specific findings rather than vague statements.
    4. Include concrete examples where useful.
    5. Identify uncertainties, assumptions, and knowledge gaps.
    6. Do not invent statistics, studies, source references, or citations.
    7. If you cannot verify a claim or provide supporting evidence,
       clearly acknowledge that limitation.
    8. Avoid researching unrelated topics or duplicating other tasks.

    Return your findings using the ResearchFinding schema.
    """


async def research_topic(topic: str, task: ResearchTask) -> ResearchFinding:
    logger.info("Starting research task: %s", task.task_name)
    logger.debug(f"Topic: {topic}")
    logger.debug(f"Research question: {task.research_question}")

    completions = await asyncClient.beta.chat.completions.parse(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},            {
            "role": "user",
            "content": f"""
                Overall Research Question:
                {topic}

                Assigned Research Task:
                {task.model_dump_json(indent=2)}

                Investigate this task and return your findings.
                """,
        }],
        response_format=ResearchFinding
    )

    message = completions.choices[0].message

    if message.parsed is None:
        raise ValueError(
            f"Research failed for task '{task.task_name}'. "
            f"Refusal: {message.refusal}"
        )

    finding = message.parsed
    logger.info("Completed research task: %s ", finding.task_name)

    return finding
