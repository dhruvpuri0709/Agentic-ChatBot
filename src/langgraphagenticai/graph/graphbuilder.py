from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.state.state import State
import streamlit as st
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tool, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticai.nodes.chatbot_with_tools import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph
        
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,'chatbot')
        self.graph_builder.add_edge('chatbot',END)
    
    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node and
        a tool node. It defines tools. initializes the chatbot with tool capablities,
        and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point. 
        """
        # Define the tool and the tool node
        tools = get_tool()
        tool_node = create_tool_node(tools)
        llm = self.llm

        # Define the chatbot node
        obj_chatbot_with_tools_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_tools_node.create_chatbot(tools)
        
        # Define the chatbot node

        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        # Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge('tools','chatbot')
        self.graph_builder.add_edge('chatbot',END)
    
    def ai_news_builder_graph(self):

        #Define the nodes

        ainews = AINewsNode(self.llm)
        
        self.graph_builder.add_node("Fetch_News",ainews.fetch_news)
        self.graph_builder.add_node("Summarize",ainews.summarize_news)
        self.graph_builder.add_node("Save_Result",ainews.save_result)

        #Define the edges
        
        self.graph_builder.set_entry_point("Fetch_News")
        self.graph_builder.add_edge(START,"Fetch_News")
        self.graph_builder.add_edge("Fetch_News","Summarize")
        self.graph_builder.add_edge("Summarize","Save_Result")
        self.graph_builder.add_edge("Save_Result", END)


        

    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With WebSearch":
            self.chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            self.ai_news_builder_graph()
        # st.write("reached setup graph")
        return self.graph_builder.compile()




