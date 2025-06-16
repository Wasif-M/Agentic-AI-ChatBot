import streamlit as st
from src.langgraph.ui.streamlitui.ui_loader import LoadStreamliUI
from src.langgraph.LLMS.groqllm import GroqLLM
from src.langgraph.graph.graph_builder import GraphBuilder
from src.langgraph.ui.streamlitui.display_result import DisplayResultStreamlit
def load_langgraph_agentai_app():
    """
    Load and runs the langgraph agentic ai app with streamli ui.
    this function initialize the ui,handle the user input,configure the LLM model,set up the 
    graph based on the selected use case , and display the ouptputs whileimplementing the excepion hadling 
    fro robutness
    """
#loadui
    ui=LoadStreamliUI()
    user_input=ui.load_ui()
    if not user_input:
        st.error("Error:Failed to load the user input from the ui")
        return
    user_message=st.chat_input("Enter the message:")

    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()
            if not model:
                st.error("Error: LLM model couldn;t be initialzed")
                return
            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("Error:No usecase selected")

                return
            
            usecase=user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected")
                return
            graph_builder=GraphBuilder(model=model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error in building the graph: {e}")
                return
        except Exception as e:
            st.error(f"Error: Graph set up failed- {e}")
            return


