from src.langgraph.state.state import State

class ChatbotWithWebSearchToolNode:
    def __init__(self,model):
        self.llm=model
    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        system_prompt = "You are a web search assistant. Use web search tools to answer user queries when appropriate."
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "system", "content": system_prompt},{"role": "user", "content": user_input}])

        # Simulate tool-specific logic
        tools_response = f"Tool integration for: '{user_input}'"

        return {"messages": [llm_response, tools_response]}
    

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function that uses the provided tools (including BraveSearch).
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Processes the input state and returns a response, using tools if needed.
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node