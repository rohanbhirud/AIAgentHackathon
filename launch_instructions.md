# AI Agent Application - Launch Instructions

## Overview
This application uses Taiga (an open-source project management tool) with AI integration components. The application runs using Docker containers orchestrated with Docker Compose.

## Prerequisites
- Docker and Docker Compose installed on your system
- Python 3.x installed
- Required Python packages (run: `pip install -r requirements.txt`)

## First-Time Launch

For the first time setup, you need to initialize the system which will:
1. Start all required Docker containers
2. Wait for the services to be ready
3. Create an admin user for Taiga

Run the initialization script:

```bash
python init.py
```

You can optionally provide custom admin credentials:

```bash
python init.py <username> <email> <password>
```

If not provided, the default credentials will be:
- Username: admin
- Email: admin@example.com
- Password: adminpassword

The initialization process may take a few minutes as it sets up all the necessary containers.

## Regular Launch (After First-Time Setup)

For subsequent launches, you can simply start the Docker containers:

```bash
docker-compose up -d
```

## Accessing the Taiga Application

Once running, the application will be available at:
- Main interface: http://localhost:8888
- Backend API: http://localhost:8080

## Stopping the Application

To stop the application:

```bash
docker-compose down
```

To stop and remove all data (warning: this will delete all your projects and data):

```bash
docker-compose down -v
```
