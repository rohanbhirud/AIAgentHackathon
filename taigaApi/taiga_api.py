import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TaigaAPI:
    """Main class for interacting with the Taiga API"""
    
    def __init__(self, username=None, password=None):
        """
        Initialize the Taiga API client
        
        Args:
            username: Taiga username (defaults to environment variable)
            password: Taiga password (defaults to environment variable)
        """
        # Load API URL from environment
        self.api_url = os.getenv("TAIGA_API_URL", "http://localhost:8080/api/v1")
        
        # Load credentials from parameters or environment
        self.username = username or os.getenv("TAIGA_USERNAME", "admin")
        self.password = password or os.getenv("TAIGA_PASSWORD", "adminpassword")
        
        # Authentication state
        self.auth_token = None
        self.refresh_token = None
        self.user_id = None
        
        print(f"✅ Taiga API client initialized with URL: {self.api_url}")
    
    def authenticate(self):
        """
        Authenticate with the Taiga API
        
        Returns:
            Boolean indicating success
        """
        try:
            url = f"{self.api_url}/auth"
            
            payload = {
                "type": "normal",
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            auth_data = response.json()
            self.auth_token = auth_data.get("auth_token")
            self.refresh_token = auth_data.get("refresh")
            self.user_id = auth_data.get("id")
            
            if self.auth_token:
                print(f"✅ Authenticated as {self.username}")
                return True
            else:
                print("❌ Authentication failed: No auth token received")
                return False
                
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    
    def refresh_authentication(self):
        """
        Refresh the authentication token
        
        Returns:
            Boolean indicating success
        """
        if not self.refresh_token:
            return self.authenticate()
        
        try:
            url = f"{self.api_url}/auth/refresh"
            
            payload = {
                "refresh": self.refresh_token
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            auth_data = response.json()
            self.auth_token = auth_data.get("auth_token")
            self.refresh_token = auth_data.get("refresh")
            
            if self.auth_token:
                print("✅ Authentication token refreshed")
                return True
            else:
                print("❌ Token refresh failed: No auth token received")
                return False
                
        except Exception as e:
            print(f"❌ Token refresh failed: {e}")
            # Fall back to full authentication
            return self.authenticate()
    
    def get_headers(self):
        """
        Get headers for API requests
        
        Returns:
            Dictionary of headers
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}" if self.auth_token else None
        }
    
    def get_user_info(self):
        """
        Get information about the authenticated user
        
        Returns:
            User data if successful, None otherwise
        """
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            url = f"{self.api_url}/users/me"
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            user_data = response.json()
            print(f"✅ Retrieved user info for {user_data.get('username')}")
            return user_data
            
        except Exception as e:
            print(f"❌ Failed to get user info: {e}")
            return None