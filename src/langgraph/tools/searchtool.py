from langchain_community.tools.brave_search.tool import BraveSearch

from langgraph.prebuilt.tool_node import ToolNode


def get_tools():
    """Return the numbers of tools to be used in the chatbot"""
    tools=[BraveSearch(max_results=2)]
    return tools
def create_toolNode(tools):
    """creates and returns a tools for the graph"""
    return ToolNode(tools=tools)
