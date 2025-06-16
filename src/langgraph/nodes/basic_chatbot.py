from src.langgraph.state.state import State


class BasicChatBotNode:
    """Basic chatbot logic implementation"""
    def __init__(self,model):
        self.llm=model
    def process(self,state: State)->dict:
        "Process the input and genrate the chatbot response"
        return {"messages":self.llm.invoke(state['messages'])}
