# Claude Golden Goose 🦢

Automate your Claude Code Vibe coding. Analyze your existing codebase, use AI to create improvement plans and detailed task lists, and drip-feed the tasks to Claude Code to build while you sleep, play, or live.

---

## 🚀 What is Claude Golden Goose?

**Claude Golden Goose** is a powerful, self-hosted Django application designed to supercharge and automate your AI-assisted development workflows with [Claude Code](https://claude.ai/code). It acts as a comprehensive control panel and automation layer, allowing you to manage everything from high-level roadmaps to granular, AI-driven task execution.

This project isn't just a single tool; it's an integrated suite of applications built to orchestrate complex software development. It allows you to analyze your codebase, generate strategic plans (PRDs, implementation plans), break them down into tasks, and then feed those tasks to Claude Code automatically.

---

## ✨ Key Features

* **Headless Claude Interface**: A web UI to interact with the Claude Code CLI. Manage conversations, prompts, and automated chat hooks.
* **Visual Workflow Engine**: Design multi-step automation flows. Chain Claude conversations, use decision nodes, and trigger sub-workflows.
* **AI-Driven Project Management**: A full-fledged **`claude_manager`** app to define your product, create roadmaps, write PRDs, and generate technical implementation plans.
* **Kanban Board**: Visualize your AI-generated (and human-managed) tasks in a drag-and-drop interface.
* **Automated Task Queue**: The "drip-feed" system. Automatically feeds tasks from your `claude_manager` plan to the `headless` Claude executor one-by-one.
* **Remote Job Execution (via Tailscale)**: A powerful REST API (**`tailscale`** app) to run jobs (Bash commands or Claude prompts) on remote nodes. Includes a client for nodes to poll for work.
* **Unified Dashboard**: A central dashboard to see statistics and overviews from all integrated apps.

---

## 🏛️ Architecture & Core Applications

This project is a Django monolith composed of several key apps:

* **`mysite`**: The main Django project, settings, root URLs, and the unified dashboard.
* **`headless`**: The core web UI for chatting with Claude Code. Manages conversations, the visual workflow engine, and the automated task queue.
* **`claude_manager`**: The "brains" of the operation. Manages the high-level development lifecycle: `ProductApp` → `Roadmap` → `PRD` → `ImplementationPlan` → `Task`. Includes Kanban boards and version history for all models.
* **`tailscale`**: A REST API and web UI for managing remote worker nodes and executing jobs (like running Claude prompts or bash scripts) on them.
* **`process`**: (Early stage) An app for AI-assisted process system design (mining/mineral processing).
* **`homebudget`**: (Skeleton) A placeholder app for a personal budgeting tool.

---

## 🏁 Getting Started

### Prerequisites

* Python 3.12+
* Django 4.2+
* Access to Claude Code CLI

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/claude-golden-goose.git](https://github.com/YOUR_USERNAME/claude-golden-goose.git)
    cd claude-golden-goose
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    *(Note: A `requirements.txt` file should be created from the project's dependencies.)*
    ```bash
    # Install key packages mentioned in the CLAUDE.md
    pip install Django==4.2.16 djangorestframework django-htmx django-crispy-forms crispy-bootstrap5 django-simple-history
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser for admin access:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  Access the application at `http://127.0.0.1:8000/`.

---

## 🛠️ Development Commands

### Basic Django Commands

```bash
# Run the development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Run all tests
python manage.py test

# Open the interactive Django shell
python manage.py shell
