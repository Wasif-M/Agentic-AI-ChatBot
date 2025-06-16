import streamlit as st
import os
from src.langgraph.ui.uiconfig import Config

class LoadStreamliUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}
    def load_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())


        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key",type="password")
                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your GROQ API key to proceed")
            
            ## USecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options)
            if self.user_controls['selected_usecase']=="Web Search Chatbot":
                os.environ["BRAVE_SEARCH_API_KEY"]=self.user_controls['BRAVE_SEARCH_API_KEY']=st.session_state["BRAVE_SEARCH_API_KEY"]=st.text_input("Brave API Key",type="password")
                if not self.user_controls["BRAVE_SEARCH_API_KEY"]:
                    st.warning("Plaese enter your Brave API key to proceed")

        return self.user_controls