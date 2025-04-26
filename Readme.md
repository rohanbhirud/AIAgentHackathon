# AI Agent Application - Launch Instructions

## Overview
This application uses Taiga (an open-source project management tool) with AI integration components. The application runs using Docker containers orchestrated with Docker Compose.

## Prerequisites
- Docker and Docker Compose installed on your system
- Python 3.x installed
- Required Python packages (run: `pip install -r requirements.txt`)

## First-Time Launch

For the first time setup, you need to run docker for taiga. Check Readme.md from taiga-docker folder


The initialization process may take a few minutes as it sets up all the necessary containers.

## Regular Launch (After First-Time Setup)

For subsequent launches, you can simply start the Docker containers:

```bash
docker-compose up -d
```

To start the agent(It will start in terminal):

```bash
python taiga_ai_agent.py
```

## Stopping the Application

To stop the application:

```bash
docker-compose down
```

To stop and remove all data (warning: this will delete all your projects and data):

```bash
docker-compose down -v
```
