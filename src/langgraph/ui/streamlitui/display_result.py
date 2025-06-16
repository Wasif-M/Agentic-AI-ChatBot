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
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content if hasattr(value["messages"], "content") else value["messages"])

        elif usecase == "Web Search Chatbot":
            # Show user's message
            with st.chat_message("user"):
                st.write(user_message)


            with st.chat_message("assistant"):
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("💭 Thinking...")
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)

          
            thinking_placeholder.empty()

            
            for message in res['messages']:
                if isinstance(message, ToolMessage):
                    if is_function_call_placeholder(message.content):
                        continue
                    parsed_results = parse_tool_response(message.content)
                    if parsed_results:
                        with st.chat_message("assistant"):
                            st.markdown("**🔎 Tool Response:**")
                            for item in parsed_results:
                                render_item(item)
                    else:
                        with st.chat_message("assistant"):
                            st.write("No valid structured tool response found.")

                elif isinstance(message, AIMessage) and message.content:
                    if is_function_call_placeholder(message.content):
                        continue
                    with st.chat_message("assistant"):
                        st.write(message.content)



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
