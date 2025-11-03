# crew_config/crew.py (CORRECTED)

from crewai import Crew, Process
from crew_config.agents import planner_agent, researcher_agent, writer_agent
from crew_config.tasks import all_tasks

class ContentCreationCrew:
    """
    Orchestrates the multi-agent collaboration process.
    """
    def __init__(self, topic: str):
        self.topic = topic
        
        updated_tasks = self.update_task_descriptions()
        
        # Define the crew (coordinator)
        self.crew = Crew(
            agents=[planner_agent, researcher_agent, writer_agent],
            tasks=updated_tasks,
            process=Process.sequential, 
            # 🛑 FIX: Change 'verbose=2' to 'verbose=True' to satisfy Pydantic validation.
            # True still provides detailed logging of agent thoughts and actions.
            verbose=True, 
        )

    def update_task_descriptions(self):
        """Helper to inject the topic into the task descriptions."""
        updated_tasks = []
        for task in all_tasks:
            # We must create a copy or new instance to update the description
            task.description = task.description.format(topic=self.topic)
            updated_tasks.append(task)
        return updated_tasks

# Note: The crew is initialized and run from main.py