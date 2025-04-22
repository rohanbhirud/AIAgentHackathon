import os
import json
from dotenv import load_dotenv
from azure_ai_client import AzureAIClient
from taigaApi.taiga_api import TaigaAPI
from taigaApi.epic_manager import EpicManager
from taigaApi.user_story_manager import UserStoryManager
import taiga_functions

# Load environment variables
load_dotenv()

class TaigaAIAgent:
    """AI Agent for creating and managing Taiga project artifacts using Azure OpenAI"""
    
    def __init__(self):
        """Initialize the Taiga AI Agent with Azure OpenAI and Taiga API clients"""
        # Initialize the Azure OpenAI client
        self.ai_client = AzureAIClient()
        
        # Initialize the Taiga API client and authenticate
        self.taiga_api = TaigaAPI()
        if not self.taiga_api.authenticate():
            print("❌ Failed to authenticate with Taiga API")
            return
            
        # Initialize Taiga managers
        self.epic_manager = EpicManager(self.taiga_api)
        self.user_story_manager = UserStoryManager(self.taiga_api)
        
        # Load tools definition
        self.tools = self._load_tools()
        
        print("✅ Taiga AI Agent initialized for default project (ID: 1)")
    
    def _load_tools(self):
        """Load the tools definition from JSON file"""
        try:
            with open('taiga_tools.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"❌ Error loading tools definition: {e}")
            return []
    
    def run_conversation(self, user_input):
        """
        Run a conversation with the AI model to process user input
        
        Args:
            user_input: User's message
            
        Returns:
            AI's response
        """
        if not self.ai_client.client:
            return "Error: Azure OpenAI client is not initialized properly."
        
        # Initial message history
        messages = [{"role": "user", "content": user_input}]
        
        # First API call: Ask the model to use the functions
        try:
            response = self.ai_client.client.chat.completions.create(
                model=self.ai_client.deployment,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
            )
            
            # Process the model's response
            response_message = response.choices[0].message
            messages.append(response_message)
            
            # Check if the model wants to call functions
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the appropriate function
                    function_response = None
                    
                    if function_name == "list_epics":
                        function_response = taiga_functions.list_epics(
                            self.taiga_api, 
                            self.epic_manager
                        )
                    elif function_name == "create_epic":
                        function_response = taiga_functions.create_epic(
                            self.taiga_api,
                            self.epic_manager,
                            function_args.get("subject"),
                            function_args.get("description"),
                            function_args.get("tags")
                        )
                    elif function_name == "update_epic":
                        function_response = taiga_functions.update_epic(
                            self.taiga_api,
                            self.epic_manager,
                            function_args.get("epic_id"),
                            function_args.get("updates")
                        )
                    elif function_name == "list_user_stories":
                        function_response = taiga_functions.list_user_stories(
                            self.taiga_api,
                            self.user_story_manager,
                            function_args.get("epic_id")
                        )
                    elif function_name == "create_user_story":
                        function_response = taiga_functions.create_user_story(
                            self.taiga_api,
                            self.user_story_manager,
                            function_args.get("subject"),
                            function_args.get("description"),
                            function_args.get("epic_id")
                        )
                    elif function_name == "update_user_story":
                        function_response = taiga_functions.update_user_story(
                            self.taiga_api,
                            self.user_story_manager,
                            function_args.get("story_id"),
                            function_args.get("updates")
                        )
                    
                    # Add function response to messages
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response
                    })
            
            # Get the final response from the model
            final_response = self.ai_client.client.chat.completions.create(
                model=self.ai_client.deployment,
                messages=messages,
            )
            
            return final_response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_interactive_session(self):
        """Start an interactive session with the AI agent"""
        print("\n🤖 Taiga AI Agent - Interactive Session")
        print("Type 'exit' or 'quit' to end the session\n")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("\nExiting Taiga AI Agent. Goodbye!")
                break
                
            response = self.run_conversation(user_input)
            print(f"\nAI: {response}")


if __name__ == "__main__":
    # Create and run the Taiga AI Agent
    agent = TaigaAIAgent()
    agent.start_interactive_session()