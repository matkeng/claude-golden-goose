# claude-golden-goose

Automate your Claude Code Vibe coding - analyzes your existing codebase, uses AI to create improvement plans, and detailed task lists, then drip-feeds the tasks to Claude Code to build while you sleep, play, or live.

## Features

- **Django 4.2.16 Framework**: Modern Python web framework for building the automation platform
- **Google Gemini Integration**: AI-powered code analysis and task generation
- **Claude (Anthropic) Integration**: Headless mode automation for executing coding tasks
- **Tailscale Support**: Remote configuration and secure access to your automation system
- **Celery Background Tasks**: Queue and process automation tasks asynchronously
- **REST API**: Full API support for integration with other tools

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (venv) or Conda
- Redis (for Celery task queue)
- PostgreSQL (optional, for production)

## Installation

### Option 1: Using Virtual Environment (venv)

1. Clone the repository:
```bash
git clone https://github.com/matkeng/claude-golden-goose.git
cd claude-golden-goose
```

2. Run the setup script:
```bash
./setup_venv.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

### Option 2: Using Conda

1. Clone the repository:
```bash
git clone https://github.com/matkeng/claude-golden-goose.git
cd claude-golden-goose
```

2. Run the setup script:
```bash
./setup_conda.sh
```

3. Activate the conda environment:
```bash
conda activate claude-golden-goose
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and configure your settings:

### Required Settings
```bash
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Claude API (Anthropic)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_HEADLESS_MODE=True
```

### Optional Settings

#### Database (PostgreSQL for production)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

#### Tailscale (for remote configuration)
```bash
TAILSCALE_ENABLED=True
TAILSCALE_HOSTNAME=your-tailscale-hostname
TAILSCALE_AUTH_KEY=your-tailscale-auth-key
TAILSCALE_API_KEY=your-tailscale-api-key
```

#### Celery (for background tasks)
```bash
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Running the Application

### 1. Apply Database Migrations
```bash
python manage.py migrate
```

### 2. Create a Superuser
```bash
python manage.py createsuperuser
```

### 3. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### 4. Run Celery Worker (for background tasks)

In a separate terminal:
```bash
celery -A claude_goose worker --loglevel=info
```

### 5. Run Celery Beat (for scheduled tasks - optional)

In a separate terminal:
```bash
celery -A claude_goose beat --loglevel=info
```

## Usage

### AI Integration

#### Using Gemini for Code Analysis

```python
from ai_integration.gemini_client import get_gemini_client

gemini = get_gemini_client()

# Analyze code
analysis = gemini.analyze_code(your_code, "Focus on security")

# Generate task list
tasks = gemini.generate_tasks(project_requirements)
```

#### Using Claude for Code Automation

```python
from ai_integration.claude_client import get_claude_client

claude = get_claude_client()

# Automate a coding task in headless mode
result = claude.automate_code_task(
    "Create a user authentication system",
    codebase_context="Django project with REST API"
)

# Review code
review = claude.review_code(code_snippet)

# Generate improvement plan
plan = claude.generate_improvement_plan(codebase_analysis)
```

### Background Task Automation

```python
from automation.tasks import (
    analyze_codebase,
    automate_coding_task,
    batch_process_tasks
)

# Queue a code analysis task
result = analyze_codebase.delay(code_content)

# Queue a coding task
result = automate_coding_task.delay(
    "Implement user login endpoint",
    codebase_context
)

# Batch process multiple tasks (drip-feed to Claude)
task_list = [
    "Create database models",
    "Implement authentication",
    "Add API endpoints"
]
result = batch_process_tasks.delay(task_list)
```

### Tailscale Integration

```python
from ai_integration.tailscale_manager import get_tailscale_manager

ts = get_tailscale_manager()

# Check if Tailscale is enabled
if ts.is_enabled():
    status = ts.get_status()
    print(f"Connected: {status['connected']}")
```

## API Endpoints

The application provides REST API endpoints for automation:

- `/admin/` - Django admin interface
- `/api/` - REST API root (requires authentication)

## Project Structure

```
claude-golden-goose/
├── ai_integration/          # AI integration app (Gemini, Claude, Tailscale)
│   ├── gemini_client.py    # Google Gemini integration
│   ├── claude_client.py    # Anthropic Claude integration
│   └── tailscale_manager.py # Tailscale remote configuration
├── automation/              # Automation app (background tasks)
│   └── tasks.py            # Celery tasks for automation
├── claude_goose/           # Django project settings
│   ├── settings.py         # Configuration
│   ├── celery.py          # Celery configuration
│   └── urls.py            # URL routing
├── logs/                   # Application logs
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── setup_venv.sh         # Virtual environment setup script
├── setup_conda.sh        # Conda environment setup script
└── .env.example          # Environment variables template
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

The project uses:
- Django Debug Toolbar (development only)
- Django REST Framework for API development
- Celery for asynchronous task processing

## Security Notes

- Never commit `.env` file with real API keys
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use PostgreSQL or another production database
- Enable HTTPS in production
- Keep all dependencies updated

## Troubleshooting

### Redis Connection Issues
Make sure Redis is running:
```bash
redis-cli ping
```

### Celery Not Processing Tasks
Check that Celery worker is running:
```bash
celery -A claude_goose inspect active
```

### API Key Errors
Verify your API keys in `.env` file and ensure they are valid.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

