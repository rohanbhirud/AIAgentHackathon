from typing import List, Dict, Any, Optional
import json

class StoryGenerator:
    """Generate user stories from epics using Azure OpenAI"""
    
    def __init__(self, taiga_api, azure_ai_client):
        """
        Initialize the Story Generator
        
        Args:
            taiga_api: Instance of TaigaAPI
            azure_ai_client: Instance of AzureAIClient
        """
        self.taiga = taiga_api
        self.ai_client = azure_ai_client
    
    def breakdown_epic_into_stories(self, project_id: Any, epic_id: Any) -> List[Dict[str, Any]]:
        """
        Analyze an epic's description and generate user stories with AI
        
        Args:
            project_id: The ID of the project
            epic_id: The ID of the epic to analyze
            
        Returns:
            List of created user stories
        """
        from taigaApi.epic_manager import EpicManager
        from taigaApi.user_story_manager import UserStoryManager
        
        # Initialize managers
        epic_manager = EpicManager(self.taiga)
        user_story_manager = UserStoryManager(self.taiga)
        
        # Get the epic details
        epic = epic_manager.get_epic(epic_id)
        if not epic:
            print(f"❌ Failed to retrieve epic with ID {epic_id}")
            return []
        
        epic_subject = epic.get("subject", "")
        epic_description = epic.get("description", "")
        
        print(f"🔍 Analyzing epic: '{epic_subject}'")
        
        # Create a prompt for the AI to generate user stories
        system_prompt = """
        You are an expert product manager who knows how to break down epics into user stories.
        Analyze the epic description and generate a set of user stories that cover the functionality described.
        Each user story should be clear, concise, and follow the format: "As a [user type], I want [action] so that [benefit]".
        Provide a detailed description for each story that elaborates on the implementation details, acceptance criteria, and any notes for developers.
        """
        
        user_prompt = f"""
        Epic Subject: {epic_subject}
        Epic Description: {epic_description}
        
        Generate 3-5 user stories that cover the functionality described in this epic.
        Return your response as a JSON array of objects with the following structure:
        [
            {{
                "subject": "Story title in user story format",
                "description": "Detailed description including acceptance criteria"
            }}
        ]
        """
        
        if not self.ai_client.client:
            print("❌ Azure OpenAI client is not initialized")
            return []
        
        try:
            # Call the Azure OpenAI API to generate user stories
            response = self.ai_client.client.chat.completions.create(
                model=self.ai_client.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the content from the response
            content = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                # Find the first opening bracket and the last closing bracket
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_content = content[start_idx:end_idx]
                    user_stories_data = json.loads(json_content)
                else:
                    # Handle case where JSON is not properly formatted
                    print("⚠️ AI response did not contain properly formatted JSON. Attempting to fix...")
                    # Simple cleanup attempt
                    json_content = content.strip().replace("```json", "").replace("```", "")
                    user_stories_data = json.loads(json_content)
            except Exception as json_error:
                print(f"❌ Failed to parse AI response as JSON: {json_error}")
                print(f"AI Response: {content}")
                return []
            
            # Create the user stories in Taiga
            created_stories = []
            for story_data in user_stories_data:
                subject = story_data.get("subject")
                description = story_data.get("description")
                
                print(f"📝 Creating user story: '{subject}'")
                
                # Create the user story (without linking to epic)
                story = user_story_manager.create_user_story(
                    project_id=project_id,
                    subject=subject,
                    description=description
                )
                
                if story:
                    # Now link the user story to the epic using the separate endpoint
                    story_id = story.get("id")
                    success = user_story_manager.link_user_story_to_epic(
                        user_story_id=story_id,
                        epic_id=epic_id
                    )
                    
                    if success:
                        print(f"🔗 Linked user story '{subject}' to epic '{epic_subject}'")
                    else:
                        print(f"⚠️ Failed to link user story '{subject}' to epic '{epic_subject}'")
                    
                    created_stories.append(story)
            
            print(f"✅ Created {len(created_stories)} user stories for epic '{epic_subject}'")
            return created_stories
            
        except Exception as e:
            print(f"❌ Error generating stories from epic: {e}")
            return []
