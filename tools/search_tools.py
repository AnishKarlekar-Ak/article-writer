# tools/search_tools.py (CORRECTED)

# Import the DuckDuckGo Search tool from the LangChain community package
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool # Import the tool decorator from CrewAI

# -------------------------------------------
# OPTION 1: Using the LangChain tool directly
# -------------------------------------------

# Initialize the DuckDuckGo search tool
# No API key needed for this tool.
search_run_tool = DuckDuckGoSearchRun()

# Use the @tool decorator to wrap the search run function 
# and make it usable by CrewAI agents.
@tool("DuckDuckGo Search Tool")
def duckduckgo_search(search_query: str) -> str:
    """
    A search tool used to query DuckDuckGo for search results when trying to find 
    current information from the internet.
    """
    # The LangChain tool's 'run' method executes the search
    return search_run_tool.run(search_query)

# A list of tools to be used by agents
# Pass the wrapped function as the tool
all_tools = [duckduckgo_search]