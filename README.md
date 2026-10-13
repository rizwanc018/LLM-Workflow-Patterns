# LLM Workflow Patterns

Small, self-contained Python examples of common LLM workflow patterns, built on the OpenAI API with Pydantic structured outputs. Each pattern lives in its own package under `src/llm_workflow_patterns/` and can be run on its own.

| Pattern | What it shows | Example scenario |
| --- | --- | --- |
| [Prompt chaining](src/llm_workflow_patterns/prompt_chaining/) | A fixed sequence of LLM calls, with a gate check between steps | Classify a support ticket, extract its details, decide a resolution, write the reply |
| [Routing](src/llm_workflow_patterns/routing/) | Classify the input, then send it to a specialised handler | Route a request to a payment, technical or account handler |
| [Parallelization](src/llm_workflow_patterns/parallelization/) | Run independent LLM checks concurrently and combine the results | Validate a support request and check it for prompt injection at the same time |
| [Orchestrator–workers](src/llm_workflow_patterns/orchestrator_workers/) | One LLM plans subtasks, workers run them in parallel, results are synthesized | Plan research tasks, research them concurrently, write and review a report |
| [Evaluator–optimizer](src/llm_workflow_patterns/evaluator_optimizer/) | One LLM generates, another evaluates, and the loop repeats until the output passes | Draft and iteratively improve a customer support reply |

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key

## Setup

```bash
uv sync
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

Settings are loaded in [config.py](src/llm_workflow_patterns/config/config.py), which also sets the model (`gpt-4o`) and creates the sync and async OpenAI clients shared by every example.

## Running the examples

```bash
uv run prompt-chaining
uv run routing
uv run parallelization
uv run orchestrator
uv run evaluator-optimizer
```
