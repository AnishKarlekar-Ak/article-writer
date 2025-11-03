# main.py

import os
from dotenv import load_dotenv
from crewai import Crew
# Import the orchestrator class which loads the Agents and Tasks
from crew_config.crew import ContentCreationCrew  

# --- IMPORTANT: Load environment variables first ---
# This must run before the subsequent imports access os.getenv()
load_dotenv() 

def run_crew():
    """Initializes and executes the Content Creation Crew."""
    
    # --- Configuration Verification ---
    # Check for the minimum required API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("🚨 CRITICAL ERROR: OPENAI_API_KEY not set in .env file.")
        print("Please verify your .env file and ensure the OpenRouter key is present.")
        exit()

    print("--- Starting Multi-Agent Content Creation Crew ---")
    
    # Get the topic from the user
    # Note: Stripping quotes entered by the user for cleaner processing
    topic = input("Enter the topic or goal for the article (e.g., 'The future of remote work'):\n> ").strip("'\"")
    
    if not topic:
        print("No topic provided. Exiting.")
        return

    # 1. Initialize the Crew Coordinator/Blueprint
    # Passes the user's topic to the crew class for task description injection
    crew_coordinator = ContentCreationCrew(topic)
    
    # 2. Kick off the autonomous process
    print(f"\n🚀 Crew is autonomously processing task: '{topic}'")
    print("-" * 50)
    
    try:
        # The kick_off method executes the tasks (Plan, Research, Write) in sequence
        result = crew_coordinator.crew.kickoff()
        
        # 3. Output the final result
        print("\n✅ Crew Process Finished! Final Output:")
        print("=" * 50)
        print(result)
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ CRITICAL FAILURE during Crew Execution: {e}")
        print("Please check the full traceback above for details on the error.")


if __name__ == "__main__":
    run_crew()