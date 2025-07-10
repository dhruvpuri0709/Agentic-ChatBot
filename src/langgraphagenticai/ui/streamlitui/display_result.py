import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        # print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    # st.write("The event in for event in graph.stream is")
                    # st.write(event)
                    for value in event.values():
                        # st.write("The value in value in event.values() is")
                        # st.write(value)
                        messages = value["messages"]
                        # print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            if isinstance(messages, list):
                                for msg in messages:
                                    st.write(msg.content)
                            else:
                                st.write(messages.content) 