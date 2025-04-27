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

## Example Prompts

1. Create a new project called "Finance Software". The project is for developing a web-based platform to manage personal and business finances, including budgeting, expense tracking, and financial reporting.

2. Create an epic in the "Finance Software" project with the subject "User Authentication Module" and description "Implement secure user registration, login, and password recovery features. Ensure support for multi-factor authentication."

3. Add an epic to the "Finance Software" project with the subject "Expense Analytics Dashboard" and description "Develop a dashboard to visualize spending patterns, generate financial reports, and provide insights using charts and graphs."

4. Break down the epic "User Authentication Module" in the "Finance Software" project into user stories. Each story should cover a specific feature such as registration, login, password recovery, and multi-factor authentication setup.

5. Break down the epic "Expense Analytics Dashboard" in the "Finance Software" project into user stories. Each story should focus on a specific dashboard feature, such as data visualization, report generation, and interactive charts for spending analysis.
