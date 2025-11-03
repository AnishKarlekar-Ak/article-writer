# crew_config/agents.py

import os
from crewai import Agent, LLM  # <<-- CRITICAL CHANGE: Import CrewAI's native LLM class
from tools.search_tools import all_tools

# --- Custom OpenRouter Header Setup ---

# Load optional headers from .env (used by LiteLLM internally)
referer_header = os.getenv("OPENROUTER_REFERER")
title_header = os.getenv("OPENROUTER_TITLE")

# --- LLM Initialization (CRITICAL FIX) ---

# We use the CrewAI LLM class, which acts as a wrapper around LiteLLM.
# LiteLLM handles the routing using the model name prefix, and the base_url.
llm_model = LLM(
    # FIX: We prepend the 'openrouter/' prefix to the full model slug.
    # This explicitly tells LiteLLM to use the OpenRouter API handler.
    model="openrouter/mistralai/mistral-small-3.2-24b-instruct:free", # <--- **THE FIX IS HERE**
    
    # Base URL must still be passed to route traffic to OpenRouter's endpoint.
    base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
    api_key="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",
    
    # We pass the custom headers and temperature via model_kwargs.
    model_kwargs={
        "temperature": 0.7,
        "extra_headers": {
            "HTTP-Referer": referer_header,
            "X-Title": title_header
        }
    }
)

# --- Agent Definitions (Remaining Agents are the same) ---

# 1. Planner Agent (The Project Manager)
planner_agent = Agent(
    role='Expert Project Planner and Article Outliner',
    goal='Develop a comprehensive, step-by-step plan and outline for the final article.',
    backstory=(
        "You are a seasoned editorial planner known for creating efficient "
        "and logical outlines. Your main objective is to structure the task "
        "to ensure the Researcher and Writer agents can work smoothly."
    ),
    llm=llm_model, # Use the correctly configured LLM instance
    verbose=True, 
    allow_delegation=False,
)

# 2. Researcher Agent (The Expert Analyst)
researcher_agent = Agent(
    role='Expert Digital Researcher and Fact Gatherer',
    goal='Retrieve and synthesize the most current, relevant, and factual information about the assigned topic.',
    backstory=(
        "You are a meticulous digital researcher with access to real-time search "
        "tools. You must only provide verified facts and summaries from your searches."
    ),
    llm=llm_model, # Use the correctly configured LLM instance
    tools=all_tools, 
    verbose=True,
    allow_delegation=False,
)

# 3. Writer Agent (The Content Creator)
writer_agent = Agent(
    role='Professional Content Writer and Editor',
    goal='Write a compelling, well-structured, and error-free article based on the Planner\'s outline and the Researcher\'s facts.',
    backstory=(
        "You are a creative writer and final editor. Your work is polished, engaging, "
        "and directly addresses the original topic goal using the provided research."
    ),
    llm=llm_model, # Use the correctly configured LLM instance
    verbose=True,
    allow_delegation=False,
)