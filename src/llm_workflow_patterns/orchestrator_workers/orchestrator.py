import logging

from llm_workflow_patterns.config.config import MODEL, client
from llm_workflow_patterns.orchestrator_workers.model import ResearchPlan

logger = logging.getLogger(__name__)

RESEARCH_PLAN_PROMPT = """
You are a research orchestrator. Your job is to analyze the user's research
question and create a structured plan for investigating it.

Research Question:
{topic}

Research Objectives:
1. Understand the key aspects of the research question.
2. Break the question into smaller, focused research tasks.
3. Assign each task a distinct objective so workers avoid unnecessary overlap.
4. Ensure the tasks collectively cover the important aspects of the topic.
5. Make each task specific enough that a worker can complete it independently.

For each research task:
- Provide a concise task name.
- Write a specific research question to investigate.
- Define the objective the worker should accomplish.
- Describe the expected output from the worker.

Planning guidelines:
- Create 3 to 5 research tasks, depending on the complexity of the topic.
- Make tasks as independent as possible so they can run in parallel.
- Avoid duplicate or overly broad tasks.
- Include different perspectives when relevant, such as technical details,
  benefits, limitations, practical applications, and risks.
- Ensure the tasks collectively address the original research question.
- Do not write the final research report yourself. Your responsibility is
  to plan the research, not execute it.

Return the result using the ResearchPlan schema.
"""


def create_research_plan(topic: str) -> ResearchPlan:
    logger.info("Creating research plan")
    logger.debug(f"Topic: {topic}")

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system",
                "content": RESEARCH_PLAN_PROMPT.format(topic=topic)},
        ],
        response_format=ResearchPlan,
    )

    message = completion.choices[0].message

    if message.parsed is None:
        error_msg = f"Failed to create research plan. Refusal: {message.refusal}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = message.parsed
    logger.info(
        "Research plan created with %d tasks",
        len(result.research_tasks),
    )
    return result
