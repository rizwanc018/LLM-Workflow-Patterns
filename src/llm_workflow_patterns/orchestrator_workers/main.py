
import asyncio

from llm_workflow_patterns.orchestrator_workers.orchestrator import create_research_plan
from llm_workflow_patterns.orchestrator_workers.reviewer import review_report
from llm_workflow_patterns.orchestrator_workers.synthesizer import synthesize_report
from llm_workflow_patterns.orchestrator_workers.worker import research_topic


async def run():
    topic = "When should developers use autonomous AI agents versus deterministic LLM workflows in production applications?"
    plan = create_research_plan(topic)
    research_findings = await asyncio.gather(
        *(research_topic(topic, task) for task in plan.research_tasks)
    )

    report = synthesize_report(topic, research_findings)
    feedback = review_report(report)

    print(feedback.model_dump_json(indent=2))


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
