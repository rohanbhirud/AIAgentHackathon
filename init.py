import subprocess
import os
import sys
import time

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

def start_docker_compose():
    """Start the Docker Compose services"""
    try:
        print("Starting Docker Compose services...")
        
        # Execute docker-compose up -d to start services in the background
        result = subprocess.run(
            "docker-compose up -d",
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Print output
        if result.stdout:
            print("\n----- DOCKER COMPOSE OUTPUT -----")
            print(result.stdout.strip())
        
        # Print errors
        if result.stderr:
            print("\n----- DOCKER COMPOSE ERRORS -----")
            print(result.stderr.strip())
        
        # Check result
        if result.returncode == 0:
            print("\n✅ Docker Compose services started successfully!")
            return True
        else:
            print(f"\n❌ Docker Compose failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Exception occurred starting Docker Compose: {e}")
        return False

def wait_for_services_ready(max_attempts=30, delay=5):
    """Wait for services to be ready before creating superuser"""
    print(f"\nWaiting for services to be ready (max {max_attempts} attempts, {delay}s delay)...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}/{max_attempts}: Checking if taiga-back is ready...")
            
            # Execute a simple command to check if the service is running
            # Using double quotes for the docker command and single quotes for the Python string
            result = subprocess.run(
                'docker exec -i taiga-back python -c "print(\'Service is running\')"',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and "Service is running" in result.stdout:
                print("✅ Services appear to be ready!")
                return True
                
        except Exception as e:
            print(f"Error checking service: {e}")
        
        print(f"Services not ready yet, waiting {delay} seconds...")
        time.sleep(delay)
    
    print("❌ Maximum attempts reached. Services may not be fully initialized.")
    return False

def initialize_system():
    """Initialize the entire system: start Docker Compose, wait for services, create superuser"""
    
    # Start Docker Compose services
    if not start_docker_compose():
        print("Failed to start Docker Compose services. Exiting.")
        return False
    
    # Wait for services to be ready
    if not wait_for_services_ready():
        print("Services did not become ready in the allowed time. Superuser creation may fail.")
        proceed = input("Do you want to try creating the superuser anyway? (y/n): ")
        if proceed.lower() != 'y':
            return False
    
    # Create superuser
    username = "admin"
    email = "admin@example.com"
    password = "adminpassword"
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        email = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    print(f"\nCreating superuser '{username}' with email '{email}'...")
    return create_superuser_direct(username, email, password)

if __name__ == "__main__":
    print("=== SYSTEM INITIALIZATION ===")
    if initialize_system():
        print("\n✅ System initialization completed successfully!")
    else:
        print("\n❌ System initialization encountered errors. Check the logs above.")