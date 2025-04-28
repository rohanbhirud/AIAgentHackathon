import requests

class EpicManager:
    def __init__(self, taiga_api):
        self.taiga = taiga_api

    def get_epics(self, project_id):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            if project_id is None:
                url = f"{self.taiga.api_url}/epics"
            else:
                url =  f"{self.taiga.api_url}/epics?project={project_id}"
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            epics = response.json()
            print(f"✅ Found {len(epics)} epics for project ID {project_id}")
            return epics
            
        except Exception as e:
            print(f"❌ Failed to get epics: {e}")
            return None
    
    def get_epic(self, epic_id):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/epics/{epic_id}"
            response = requests.get(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            epic = response.json()
            print(f"✅ Retrieved epic '{epic.get('subject')}'")
            return epic
            
        except Exception as e:
            print(f"❌ Failed to get epic details: {e}")
            return None
    
    def create_epic(self, project_id, subject, description=None, assigned_to=None, tags=None):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        try:
            url = f"{self.taiga.api_url}/epics"
            
            payload = {
                "project": project_id,
                "subject": subject,
                "description": description or "",
                "tags": tags or []
            }
            
            if assigned_to:
                payload["assigned_to"] = assigned_to
            
            response = requests.post(url, headers=self.taiga.get_headers(), json=payload)
            response.raise_for_status()
            epic = response.json()
            print(f"✅ Created epic '{subject}'")
            return epic
            
        except Exception as e:
            print(f"❌ Failed to create epic: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def update_epic(self, epic_id, updates):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return None
        
        try:
            url = f"{self.taiga.api_url}/epics/{epic_id}"
            
            response = requests.patch(url, headers=self.taiga.get_headers(), json=updates)
            response.raise_for_status()
            epic = response.json()
            print(f"✅ Updated epic '{epic.get('subject')}'")
            return epic
            
        except Exception as e:
            print(f"❌ Failed to update epic: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def delete_epic(self, epic_id):
        if not self.taiga.auth_token:
            if not self.taiga.authenticate():
                return False

        try:
            url = f"{self.taiga.api_url}/epics/{epic_id}"
            response = requests.delete(url, headers=self.taiga.get_headers())
            response.raise_for_status()
            print(f"\u2705 Deleted epic with ID {epic_id}")
            return True
        except Exception as e:
            print(f"\u274c Failed to delete epic: {e}")
            return False