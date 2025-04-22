import subprocess
import os
import sys
from taigaApi.project_manager import ProjectManager

def create_superuser_direct(username, email, password):
    """Create a superuser for Taiga using Django's management command"""
    try:
        print(f"Creating superuser with username: {username}, email: {email}")
        
        # Use proper shell quoting to avoid syntax errors
        create_cmd = f"""docker exec -i taiga-back bash -c "DJANGO_SUPERUSER_USERNAME='{username}' DJANGO_SUPERUSER_EMAIL='{email}' DJANGO_SUPERUSER_PASSWORD='{password}' python manage.py createsuperuser --noinput" """
        
        result = subprocess.run(
            create_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Print output
        if result.stdout:
            print("\n----- SUPERUSER CREATION OUTPUT -----")
            print(result.stdout.strip())
        
        # Print errors
        if result.stderr:
            print("\n----- SUPERUSER CREATION ERRORS -----")
            print(result.stderr.strip())
        
        # Check result
        if result.returncode == 0:
            print(f"\n✅ Superuser '{username}' created successfully!")
            return True
        else:
            print(f"\n❌ Superuser creation failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Exception occurred creating superuser: {e}")
        return False

def create_default_project(taiga_api):
    """Create a default project for Requirement Analyzer"""
    try:
        project_manager = ProjectManager(taiga_api)
        
        # Create the default project
        project = project_manager.create_project(
            name="Requirement Analyzer",
            description="Requirement analyzer project"
        )
        
        if project:
            print(f"\n✅ Default project 'Requirement Analyzer' created successfully!")
            return True
        else:
            print("\n❌ Default project creation failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Exception occurred creating default project: {e}")
        return False
    
def initialize_system():
    # Create superuser
    username = os.getenv("TAIGA_USERNAME", "admin")
    email = os.getenv("TAIGA_MAIL" , "admin@example.com")
    password = os.getenv("TAIGA_PASSWORD", "adminpassword")
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        email = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    superuser_created = create_superuser_direct(username, email, password)
    
    # If the Taiga API is available, try to create the default project
    if True:
        print("\nCreating default project...")
        from taigaApi.taiga_api import TaigaAPI  # Import here to avoid circular imports
        
        # Initialize TaigaAPI with the superuser credentials
        taiga_api = TaigaAPI(username=username, password=password)
        if taiga_api.authenticate():
            project_created = create_default_project(taiga_api)
            return superuser_created and project_created
    
    return superuser_created

if __name__ == "__main__":
    print("=== SYSTEM INITIALIZATION ===")
    if initialize_system():
        print("\n✅ System initialization completed successfully!")
    else:
        print("\n❌ System initialization encountered errors. Check the logs above.")