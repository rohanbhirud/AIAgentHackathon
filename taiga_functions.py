import json
import requests

def list_epics(epic_manager, project_id):
    try:
        epics = epic_manager.get_epics(project_id)
        if epics is None:
            return json.dumps({"status": "error", "message": f"Error retrieving epics for project {project_id}"})

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

def create_epic(epic_manager, subject, project_id, description=None, tags=None):
    try:
        epic = epic_manager.create_epic(
            project_id=project_id,
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

def update_epic(epic_manager, epic_id, updates):
    try:
        epic_id = int(epic_id)
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

def list_user_stories(user_story_manager):
    try:
        stories = user_story_manager.get_user_stories()
        
        if stories is None:
            return json.dumps({"status": "error", "message": "Error retrieving user stories"})
            
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

def create_user_story(user_story_manager, subject, project_id ,description=None):
    try:
        epic_id = int(epic_id) if epic_id else None
        story = user_story_manager.create_user_story(
            subject=subject,
            project_id=project_id,
            description=description
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

def list_projects(project_manager):
    try:
        projects = project_manager.get_projects()
        if projects is None:
            return json.dumps({"status": "error", "message": "Error retrieving projects"})

        formatted_projects = []
        for project in projects:
            formatted_projects.append({
                "id": project.get("id"),
                "name": project.get("name"),
                "description": project.get("description", "").replace("<p>", "").replace("</p>", "") if project.get("description") else ""
            })
            
        return json.dumps({
            "status": "success", 
            "projects": formatted_projects,
            "count": len(formatted_projects)
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def get_project(project_manager, project_id):
    try:
        project_id = int(project_id)
        project = project_manager.get_project(project_id)
        
        if not project:
            return json.dumps({"status": "error", "message": f"Failed to retrieve project {project_id}"})
            
        return json.dumps({
            "status": "success",
            "project": {
                "id": project.get("id"),
                "name": project.get("name"),
                "description": project.get("description", "").replace("<p>", "").replace("</p>", "") if project.get("description") else "",
                "members": len(project.get("members", [])),
                "total_milestones": project.get("total_milestones", 0),
                "total_story_points": project.get("total_story_points", 0)
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def create_project(project_manager, name, description=None):
    try:
        project = project_manager.create_project(name, description or "")
        
        if not project:
            return json.dumps({"status": "error", "message": f"Failed to create project '{name}'"})
            
        return json.dumps({
            "status": "success",
            "project": {
                "id": project.get("id"),
                "name": project.get("name"),
                "permalink": project.get("permalink", "")
            }
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def breakdown_epic(story_generator, epic_id, project_id):
    try:
        project_id = int(project_id)
        epic_id = int(epic_id)
        stories = story_generator.breakdown_epic_into_stories(project_id, epic_id)
        
        if not stories:
            return json.dumps({"status": "error", "message": f"Failed to break down epic {epic_id}"})
            
        formatted_stories = []
        for story in stories:
            formatted_stories.append({
                "id": story.get("id"),
                "subject": story.get("subject"),
                "permalink": story.get("permalink", "")
            })
            
        return json.dumps({
            "status": "success",
            "user_stories": formatted_stories,
            "count": len(formatted_stories)
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def link_user_story_to_epic(user_story_manager, user_story_id, epic_id):
    try:
        user_story_id = int(user_story_id)
        epic_id = int(epic_id)
        success = user_story_manager.link_user_story_to_epic(user_story_id, epic_id)
        
        if not success:
            return json.dumps({"status": "error", "message": f"Failed to link user story {user_story_id} to epic {epic_id}"})
            
        return json.dumps({
            "status": "success",
            "message": f"User story {user_story_id} linked to epic {epic_id}"
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def delete_epic(epic_manager, epic_id):
    try:
        success = epic_manager.delete_epic(epic_id)
        if not success:
            return json.dumps({"status": "error", "message": f"Failed to delete epic {epic_id}"})

        return json.dumps({"status": "success", "message": f"Epic {epic_id} deleted successfully"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def delete_project(project_manager, project_id):
    try:
        success = project_manager.delete_project(project_id)
        if not success:
            return json.dumps({"status": "error", "message": f"Failed to delete project {project_id}"})

        return json.dumps({"status": "success", "message": f"Project {project_id} deleted successfully"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def delete_user_story(user_story_manager, user_story_id):
    try:
        success = user_story_manager.delete_user_story(user_story_id)
        if not success:
            return json.dumps({"status": "error", "message": f"Failed to delete user story {user_story_id}"})

        return json.dumps({"status": "success", "message": f"User story {user_story_id} deleted successfully"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})