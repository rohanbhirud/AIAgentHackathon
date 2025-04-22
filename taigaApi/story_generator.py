from typing import List, Dict, Any, Optional

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
    
    def breakdown_epic_into_stories(self, project_id: Any, epic_id: Any) -> Optional[List[Dict[str, Any]]]:
        """
        Break down an epic into user stories using Azure OpenAI
        
        Args:
            project_id: Project ID
            epic_id: Epic ID
            
        Returns:
            List of created user stories if successful, None otherwise
        """
        # Get the epic details
        epic = self.taiga.get_epic(epic_id)
        if not epic:
            return None
        
        epic_subject = epic.get("subject", "")
        epic_description = epic.get("description", "")
        
        print(f"Breaking down epic: {epic_subject}")
        
        # Use Azure OpenAI to analyze the epic and generate user stories
        system_message = """You are an expert Agile product manager that breaks down epics into clear, actionable user stories.
For each user story, provide:
1. A clear subject line (the user story)
2. A detailed description
3. Acceptance criteria (3-5 items)
4. Estimated story points (1, 2, 3, 5, 8, 13)
5. Priority (High, Medium, Low)"""

        user_message = f"Epic: {epic_subject}\n\nDescription: {epic_description}\n\nBreak this epic down into 3-7 user stories."
        
        response = self.ai_client.chat_completion(
            system_message=system_message,
            user_message=user_message
        )
        print(f"AI response: {response}")
        if not response:
            print("❌ AI analysis failed, cannot break down epic")
            return None
        
        # Parse the response to extract user stories
        analysis_result = self.ai_client.parse_user_stories_from_response(response)
        # print(analysis_result)
        # Create user stories based on the AI analysis
        created_stories = []
        user_stories = analysis_result.get("user_stories", [])
        
        if not user_stories:
            return None
        
        print(f"Creating {len(user_stories)} user stories from AI analysis...")
        
        for story_data in user_stories:
            print(story_data)
            subject = story_data.get("subject", "")
            description = story_data.get("description", "")
            acceptance_criteria = story_data.get("acceptance_criteria", [])
            story_points = story_data.get("story_points")
            priority = story_data.get("priority")
            
            # Format the description with all the metadata
            extended_description = description
            
            if acceptance_criteria:
                criteria_text = "\n".join([f"- {item}" for item in acceptance_criteria])
                extended_description += f"\n\n### Acceptance Criteria\n{criteria_text}"
            
            if story_points:
                extended_description += f"\n\n### Story Points\n{story_points}"
            
            if priority:
                extended_description += f"\n\n### Priority\n{priority}"
            
            # Create the user story and link it to the epic
            story = self.taiga.create_user_story(
                project_id=project_id,
                subject=subject,
                description=extended_description,
                epic_id=epic_id
            )
            
            if story:
                created_stories.append(story)
        
        print(f"✅ Created {len(created_stories)} user stories for epic {epic_id}")
        return created_stories