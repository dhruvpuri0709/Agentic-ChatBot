from src.langgraphagenticai.state.state import State
import streamlit as st


class BasicChatbotNode:
    """
    Basic Chatbot login implementation
    """

    def __init__(self,model):
        self.llm=model
    
    def process(self,state:State)-> dict:
        """
        Process the input state nad generate a chatbot response
        
        """
        response = self.llm.invoke(state['messages'])
        # st.write(f"the response is {response}")
        return {"messages":[response]}
    