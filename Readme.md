# AI Agent Application - Launch Instructions

## Overview
This application uses Taiga (an open-source project management tool) with AI integration components. The application runs using Docker containers orchestrated with Docker Compose.

## Prerequisites
- Docker and Docker Compose installed on your system
- Python 3.x installed
- Required Python packages (run: `pip install -r requirements.txt`)

## First-Time Launch

For the first-time setup, you need to run Docker for Taiga. Check [Readme.md from taiga-docker folder](../taiga-docker/Readme.md).


The initialization process may take a few minutes as it sets up all the necessary containers.

## Regular Launch (After First-Time Setup)

For subsequent launches, you can simply start the Docker containers:

```bash
docker-compose up -d
```
Add below environment variables in .env file
```txt
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
```

To start the agent(It will start in terminal):

```bash
python requirement_analyzer_agent.py
```

To start the agent(It will start in Web UI at : http://127.0.0.1:5000/):

```bash
python frontend/app.py
```

## Demo

[Watch the demo video](demo_video/Requirement_Analyzer_AI_Agent_Demo.mp4)

<video width="640" height="360" controls>
  <source src="demo_video/Requirement_Analyzer_AI_Agent_Demo.mp4" type="video/mp4">
</video>

## Stopping the Application

To stop the application:

```bash
docker-compose down
```

To stop and remove all data (warning: this will delete all your projects and data):

```bash
docker-compose down -v
```

## Example Prompts

1. I want to create a new project called "Finance Software". This project should help users manage both personal and business finances. It will include features like budgeting, tracking expenses, and generating financial reports.

2. Please create an epic in the "Finance Software" project. The epic should be titled "User Authentication Module" and its description should be: "Build secure user registration, login, and password recovery. Add support for multi-factor authentication to keep accounts safe."

3. Create another epic in the "Finance Software" project called "Expense Analytics Dashboard". The description should be: "Create a dashboard that lets users see their spending patterns, generate reports, and view insights with interactive charts and graphs."

4. Can you break down the "User Authentication Module" epic in the "Finance Software" project into user stories? Each story should focus on a specific feature, like registration, login, password recovery, or setting up multi-factor authentication.

5. Now, break down the "Expense Analytics Dashboard" epic into user stories as well. Each story should cover a key dashboard feature, such as data visualization, report generation, or interactive charts for analyzing spending.
