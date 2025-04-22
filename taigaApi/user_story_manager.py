import requests

class UserStoryManager:
    """
    Manages operations related to user stories in Taiga
    """
    
    def __init__(self, taiga_api):
        """
        Initialize the User Story Manager
        
        Args:
            taiga_api: Instance of TaigaAPI
        """
        self.taiga = taiga_api
    
    def get_user_stories(self, project_id, epic_id=None):
        """
        Get user stories for a project, optionally filtered by epic
        
        Args:
            project_id: Project ID
            epic_id: Epic ID (optional)
            
        Returns:
            List of user stories if successful, None otherwise
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/userstories?project={project_id}"
            
            if epic_id:
                url = f"{url}&epic={epic_id}"
                
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            stories = response.json()
            
            if epic_id:
                print(f"✅ Found {len(stories)} user stories for epic ID {epic_id}")
            else:
                print(f"✅ Found {len(stories)} user stories for project ID {project_id}")
                
            return stories
            
        except Exception as e:
            print(f"❌ Failed to get user stories: {e}")
            return None
    
    def create_user_story(self, project_id, subject, description=None, epic_id=None, 
                          assigned_to=None, tags=None, status=None, points=None):
        """
        Create a new user story in a project
        
        Args:
            project_id: Project ID
            subject: Story title/subject
            description: Story description (can be HTML)
            epic_id: Epic ID to link the story to
            assigned_to: User ID to assign the story to
            tags: List of tags
            status: Status ID
            points: Dictionary of role-points values
            
        Returns:
            User story data if successful, None otherwise
        """
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
            
            if epic_id:
                payload["epics"] = [{"id": epic_id}]
            
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
            # First, get the current story to check if it's already linked
            url = f"{self.taiga.api_url}/userstories/{user_story_id}"
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            story = response.json()
            
            # Check if already linked
            already_linked = False
            current_epics = story.get("epics", [])
            for epic in current_epics:
                if epic.get("id") == epic_id:
                    already_linked = True
                    break
            
            if already_linked:
                print(f"✅ User story {user_story_id} is already linked to epic {epic_id}")
                return True
            
            # Add the new epic link
            current_epics.append({"id": epic_id})
            
            # Update the story with the new epic links
            update_url = f"{self.taiga.api_url}/userstories/{user_story_id}"
            
            payload = {
                "epics": current_epics
            }
            
            response = requests.patch(update_url, headers=self.taiga.get_headers(), json=payload)
            response.raise_for_status()
            print(f"✅ Linked user story {user_story_id} to epic {epic_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to link user story to epic: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False