from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic with tools integration
    """

    def __init__(self,model):
        self.llm= model

    def create_chatbot(self,tools):
        """
        Returns a chatbot node function
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot will return the response
            """
            return {"messages": [llm_with_tools.invoke(state['messages'])]}
        return chatbot_node
    
