import json
import requests

# Default project ID to use for all operations
DEFAULT_PROJECT_ID = 1

def list_epics(taiga_api, epic_manager):
    """
    List epics for the default project (ID: 1)
    
    Args:
        taiga_api: The TaigaAPI instance
        epic_manager: The EpicManager instance
        
    Returns:
        JSON string with epic details
    """
    try:
        epics = epic_manager.get_epics(DEFAULT_PROJECT_ID)
        if epics is None:
            return json.dumps({"status": "error", "message": "Error retrieving epics for default project"})

        formatted_epics = []
        for epic in epics:
            formatted_epics.append({
                "id": epic.get("id"),
                "subject": epic.get("subject")
            })
            
        return json.dumps({
            "status": "success", 
            "epics": formatted_epics,
            "count": len(formatted_epics)
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def create_epic(taiga_api, epic_manager, subject, description=None, tags=None):
    """
    Create a new epic in the default project (ID: 1)
    
    Args:
        taiga_api: The TaigaAPI instance
        epic_manager: The EpicManager instance
        subject: The title of the epic
        description: Optional description
        tags: Optional list of tags
        
    Returns:
        JSON string with the created epic details
    """
    try:
        # Create the epic
        epic = epic_manager.create_epic(
            project_id=DEFAULT_PROJECT_ID,
            subject=subject,
            description=description,
            tags=tags
        )
        
        if not epic:
            return json.dumps({"status": "error", "message": "Failed to create epic"})
            
        return json.dumps({
            "status": "success",
            "epic": {
                "id": epic.get("id"),
                "subject": epic.get("subject"),
                "url": epic.get("permalink", "")
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def update_epic(taiga_api, epic_manager, epic_id, updates):
    """
    Update an existing epic
    
    Args:
        taiga_api: The TaigaAPI instance
        epic_manager: The EpicManager instance
        epic_id: The ID of the epic to update
        updates: Dictionary with fields to update (subject, description, etc.)
        
    Returns:
        JSON string with the updated epic details
    """
    try:
        # Convert epic_id to integer
        epic_id = int(epic_id)
        
        # Update the epic
        epic = epic_manager.update_epic(epic_id, updates)
        
        if not epic:
            return json.dumps({"status": "error", "message": f"Failed to update epic {epic_id}"})
            
        return json.dumps({
            "status": "success",
            "epic": {
                "id": epic.get("id"),
                "subject": epic.get("subject"),
                "url": epic.get("permalink", "")
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def list_user_stories(taiga_api, user_story_manager, epic_id=None):
    """
    List user stories for the default project (ID: 1), optionally filtered by epic
    
    Args:
        taiga_api: The TaigaAPI instance
        user_story_manager: The UserStoryManager instance
        epic_id: Optional epic ID to filter stories
        
    Returns:
        JSON string with user story details
    """
    try:
        # Convert epic_id to integer if provided
        epic_id = int(epic_id) if epic_id else None
        
        # Get user stories
        stories = user_story_manager.get_user_stories(DEFAULT_PROJECT_ID, epic_id)
        
        if stories is None:
            return json.dumps({"status": "error", "message": "Error retrieving user stories"})
            
        # Extract relevant information for each story
        formatted_stories = []
        for story in stories:
            formatted_stories.append({
                "id": story.get("id"),
                "subject": story.get("subject"),
                "description": story.get("description", "").replace("<p>", "").replace("</p>", "")[:100] + "..." if story.get("description") else "",
                "status": story.get("status_extra_info", {}).get("name", "Unknown")
            })
            
        return json.dumps({
            "status": "success", 
            "user_stories": formatted_stories,
            "count": len(formatted_stories)
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def create_user_story(taiga_api, user_story_manager, subject, description=None, epic_id=None):
    """
    Create a new user story in the default project (ID: 1)
    
    Args:
        taiga_api: The TaigaAPI instance
        user_story_manager: The UserStoryManager instance
        subject: The title of the user story
        description: Optional description
        epic_id: Optional epic ID to link the story to
        
    Returns:
        JSON string with the created user story details
    """
    try:
        # Convert epic_id to integer if provided
        epic_id = int(epic_id) if epic_id else None
        
        # Create the user story
        story = user_story_manager.create_user_story(
            project_id=DEFAULT_PROJECT_ID,
            subject=subject,
            description=description,
            epic_id=epic_id
        )
        
        if not story:
            return json.dumps({"status": "error", "message": "Failed to create user story"})
            
        return json.dumps({
            "status": "success",
            "user_story": {
                "id": story.get("id"),
                "subject": story.get("subject"),
                "url": story.get("permalink", "")
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def update_user_story(taiga_api, user_story_manager, story_id, updates):
    """
    Update an existing user story
    
    Args:
        taiga_api: The TaigaAPI instance
        user_story_manager: The UserStoryManager instance
        story_id: The ID of the user story to update
        updates: Dictionary with fields to update (subject, description, etc.)
        
    Returns:
        JSON string with the updated user story details
    """
    try:
        # Convert story_id to integer
        story_id = int(story_id)
        
        # Update the user story
        response = requests.patch(
            f"{taiga_api.api_url}/userstories/{story_id}",
            headers=taiga_api.get_headers(),
            json=updates
        )
        response.raise_for_status()
        story = response.json()
        
        return json.dumps({
            "status": "success",
            "user_story": {
                "id": story.get("id"),
                "subject": story.get("subject"),
                "url": story.get("permalink", "")
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})