import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import html
import re

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
    
    def display_result_on_ui(self):
    
        current_key = f"{self.usecase}_{st.session_state.get('selected_llm', 'default')}_{st.session_state.get('selected_model', 'default')}"
        
        if 'current_interaction_key' not in st.session_state or st.session_state.current_interaction_key != current_key:
            st.session_state.current_interaction_key = current_key
            
            st.session_state.messages = []
        
            if hasattr(st.session_state, 'web_search_messages'):
                del st.session_state.web_search_messages
           
            if hasattr(st.session_state, 'basic_chatbot_messages'):
                del st.session_state.basic_chatbot_messages

        
        if self.usecase == "Web Search Chatbot":
           
            if 'web_search_messages' not in st.session_state:
                st.session_state.web_search_messages = []
            messages_to_display = st.session_state.web_search_messages
        elif self.usecase == "Basic Chatbot":
            
            if 'basic_chatbot_messages' not in st.session_state:
                st.session_state.basic_chatbot_messages = []
            messages_to_display = st.session_state.basic_chatbot_messages
        else:
            
            messages_to_display = st.session_state.messages

        
        user_message_entry = {"role": "user", "content": self.user_message}
        messages_to_display.append(user_message_entry)

        
        st.empty()

        
        for message in messages_to_display:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if self.usecase == "Basic Chatbot":
            
            with st.chat_message("assistant"):
                generating_placeholder = st.empty()
                generating_placeholder.markdown("🤖 Generating...")

            #
            full_response = ""
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                for event in self.graph.stream({'messages': ("user", self.user_message)}):
                    for value in event.values():
                        chunk = value["messages"].content if hasattr(value["messages"], "content") else value["messages"]
                        full_response += chunk
                        response_placeholder.markdown(full_response)
                
                
                generating_placeholder.empty()
                
                #
                st.session_state.basic_chatbot_messages.append({"role": "assistant", "content": full_response})

        elif self.usecase == "Web Search Chatbot":
            # Show thinking state
            with st.chat_message("assistant"):
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("💭 Thinking...")
            
            initial_state = {"messages": [HumanMessage(content=self.user_message)]}
            res = self.graph.invoke(initial_state)
            
            thinking_placeholder.empty()
            
            # Process and display responses
            full_ai_response = ""
            tool_responses = []

            for message in res['messages']:
                if isinstance(message, ToolMessage):
                    if is_function_call_placeholder(message.content):
                        continue
                    parsed_results = parse_tool_response(message.content)
                    if parsed_results:
                        tool_responses.extend(parsed_results)

                elif isinstance(message, AIMessage) and message.content:
                    if is_function_call_placeholder(message.content):
                        continue
                    full_ai_response += message.content

            
            st.session_state.web_search_messages = [user_message_entry]

            
            if tool_responses:
                with st.chat_message("assistant"):
                    st.markdown("**🔎 Tool Responses:**")
                    for item in tool_responses:
                        render_item(item)
                    
                    st.session_state.web_search_messages.append({
                        "role": "assistant", 
                        "content": "**🔎 Tool Responses:**\n" + "\n".join([
                            f"- {item.get('title', 'Untitled')}" for item in tool_responses
                        ])
                    })

            
            if full_ai_response:
                with st.chat_message("assistant"):
                    st.write(full_ai_response)
                
                
                st.session_state.web_search_messages.append({
                    "role": "assistant", 
                    "content": full_ai_response
                })

def parse_tool_response(content):
    try:
        if isinstance(content, list):
            return content
        data = json.loads(content)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            return []
    except Exception:
        return []

def render_item(item):
    if isinstance(item, dict):
        title = clean_html(item.get("title", ""))
        link = item.get("link", "")
        snippet = clean_html(item.get("snippet", ""))
        other_info = {k: v for k, v in item.items() if k not in {"title", "link", "snippet"}}

        if title and link:
            st.markdown(f"- [{title}]({link})")
        elif title:
            st.markdown(f"- **{title}**")
        if snippet:
            st.markdown(f"  {snippet}")

        if other_info:
            with st.expander("More details"):
                st.json(other_info)

def clean_html(text):
    if not isinstance(text, str):
        return text
    text = html.unescape(text)
    text = re.sub(r"</?strong>", "**", text)
    text = re.sub(r"</?em>", "*", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text

def is_function_call_placeholder(text):
    if isinstance(text, str):
        return text.strip().startswith("<function=") and text.strip().endswith(">")
    return False
