# crew_config/tasks.py

from crewai import Task
from crewai.tasks import TaskOutput
from crew_config.agents import planner_agent, researcher_agent, writer_agent

# --- Task Definitions ---

# 1. Planning Task (Assigned to the Planner Agent)
plan_task = Task(
    description=(
        "Based on the Topic: '{topic}', create a detailed article outline. "
        "The outline must include a title, 5-7 main sections, and specific "
        "questions or research points for the Researcher Agent to answer for each section."
    ),
    expected_output="A full, structured, multi-section article outline ready for research.",
    agent=planner_agent,
    context=[], # No context needed initially, as this starts the process
)

# 2. Research Task (Assigned to the Researcher Agent)
research_task = Task(
    description=(
        "Using the **Outline from the Planner**, conduct comprehensive web research. "
        "For each section in the outline, find and summarize **3-5 key facts or data points** "
        "that directly answer the specific research points provided in the outline. "
        "Deliver the output as a factual summary, citing sources where appropriate."
    ),
    expected_output="A comprehensive, multi-section summary of facts and research data.",
    agent=researcher_agent,
    context=[plan_task], # This task uses the output of the plan_task as its input/context
)

# 3. Writing Task (Assigned to the Writer Agent)
writing_task = Task(
    description=(
        "Write a complete, professional, and engaging article. "
        "Use the **Outline from the Planner** for structure and strictly incorporate **ALL** "
        "the factual information provided by the Researcher Agent. The tone should be informative "
        "and accessible. The final output must be the complete article text."
    ),
    expected_output="The final, polished article text, ready for publication.",
    agent=writer_agent,
    context=[plan_task, research_task], # This task uses both the outline and the research
)

# Group all tasks for the crew coordinator
all_tasks = [plan_task, research_task, writing_task]