from langgraph.graph import StateGraph,END,START
from src.langgraph.state.state import State
from src.langgraph.nodes.basic_chatbot import BasicChatBotNode
class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)
    def basic_chatbot_buil_graph(self):
        """Build basic chatbot using langgraph"""

        self.basic_chatbot=BasicChatBotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def setup_graph(self,usecase:str):
        if usecase =="Basic Chatbot":
            self.basic_chatbot_buil_graph()

        return self.graph_builder.compile()

