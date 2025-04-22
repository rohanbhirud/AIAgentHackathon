import requests

class ProjectManager:
    """
    Manages operations related to projects in Taiga
    """
    
    def __init__(self, taiga_api):
        """
        Initialize the Project Manager
        
        Args:
            taiga_api: Instance of TaigaAPI
        """
        self.taiga = taiga_api
    
    def create_project(self, name, description):
        """
        Create a new project in Taiga
        
        Args:
            name: Project name (required)
            description: Project description (required)
            
        Returns:
            Project data if successful, None otherwise
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/projects"
            
            payload = {
                "name": name,
                "description": description
            }
            
            response = requests.post(url, headers=self.taiga.get_headers(), json=payload)
            response.raise_for_status()
            project = response.json()
            print(f"✅ Created project '{name}'")
            return project
            
        except Exception as e:
            print(f"❌ Failed to create project: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def get_projects(self):
        """
        Get all projects for the authenticated user
        
        Returns:
            List of projects if successful, None otherwise
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/projects"
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            projects = response.json()
            print(f"✅ Found {len(projects)} projects")
            return projects
            
        except Exception as e:
            print(f"❌ Failed to get projects: {e}")
            return None
    
    def get_project(self, project_id):
        """
        Get details for a specific project
        
        Args:
            project_id: Project ID
            
        Returns:
            Project data if successful, None otherwise
        """
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/projects/{project_id}"
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            project = response.json()
            print(f"✅ Retrieved project '{project.get('name')}'")
            return project
            
        except Exception as e:
            print(f"❌ Failed to get project details: {e}")
            return None