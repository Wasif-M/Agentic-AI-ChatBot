from langgraph.graph import StateGraph,END,START
from src.langgraph.state.state import State
from src.langgraph.nodes.basic_chatbot import BasicChatBotNode
from src.langgraph.tools.searchtool import get_tools,create_toolNode
from langgraph.prebuilt.tool_node import ToolNode,tools_condition

from src.langgraph.nodes.chatbot_with_websearch import ChatbotWithWebSearchToolNode
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
        return self.graph_builder.compile()
    def graph_with_Web_search(self):
        """Build and advanced chatbot with tools integration"""
        tools=get_tools()
        tool_node=create_toolNode(tools)
        llm=self.llm



        
        #chatbot initilization
        obj_chatbot_with_node=ChatbotWithWebSearchToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)


        # add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)



    def setup_graph(self,usecase:str):
        if usecase =="Basic Chatbot":
            self.basic_chatbot_buil_graph()
        if usecase == "Web Search Chatbot":
            self.graph_with_Web_search()
        return self.graph_builder.compile()
