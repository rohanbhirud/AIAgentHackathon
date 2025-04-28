import requests

class UserStoryManager:
    def __init__(self, taiga_api):
        self.taiga = taiga_api
    
    def get_user_stories(self):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/userstories"  
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            stories = response.json()
                
            return stories
            
        except Exception as e:
            print(f"❌ Failed to get user stories: {e}")
            return None
    
    def create_user_story(self, subject, project_id, description=None,
                          assigned_to=None, tags=None, status=None, points=None):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/userstories"
            
            payload = {
                "project": project_id,
                "subject": subject,
                "description": description or ""
            }
            
            if assigned_to:
                payload["assigned_to"] = assigned_to
                
            if tags:
                payload["tags"] = tags
                
            if status:
                payload["status"] = status
                
            if points:
                payload["points"] = points
            
            response = requests.post(url, headers=self.taiga.get_headers(), json=payload)
            response.raise_for_status()
            story = response.json()
            print(f"✅ Created user story '{subject}'")
            return story
            
        except Exception as e:
            print(f"❌ Failed to create user story: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def link_user_story_to_epic(self, user_story_id, epic_id):
        """
        Link an existing user story to an epic
        
        Args:
            user_story_id: User story ID
            epic_id: Epic ID
            
        Returns:
            Boolean indicating success
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return False
        
        try:
            # Use the dedicated endpoint for linking user stories to epics
            url = f"{self.taiga.api_url}/epics/{epic_id}/related_userstories"
            
            payload = {
                "epic": epic_id,
                "user_story": user_story_id
            }
            
            response = requests.post(url, headers=self.taiga.get_headers(), json=payload)
            response.raise_for_status()
            print(f"✅ Linked user story {user_story_id} to epic {epic_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to link user story to epic: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False

    def delete_user_story(self, user_story_id):
        """
        Delete a user story by its ID

        Args:
            user_story_id: User story ID

        Returns:
            Boolean indicating success
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return False

        try:
            url = f"{self.taiga.api_url}/userstories/{user_story_id}"
            response = requests.delete(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            print(f"\u2705 Deleted user story with ID {user_story_id}")
            return True
        except Exception as e:
            print(f"\u274c Failed to delete user story: {e}")
            return False