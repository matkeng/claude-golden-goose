# Quick Start Guide

## Installation Complete! 🎉

This guide will help you get started with Claude Golden Goose.

## Step 1: Configure API Keys

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # Required for AI features
   GEMINI_API_KEY=your-actual-gemini-api-key
   ANTHROPIC_API_KEY=your-actual-anthropic-api-key
   
   # Optional: For production, change the secret key
   SECRET_KEY=your-secure-secret-key
   ```

### Getting API Keys

- **Google Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Anthropic Claude**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

## Step 2: Initialize the Database

```bash
# Apply migrations (already done if you ran test_installation.py)
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser
```

## Step 3: Start the Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Step 4: (Optional) Start Celery for Background Tasks

In a separate terminal:

```bash
# Make sure Redis is running first
# On Ubuntu/Debian: sudo service redis-server start
# On macOS: brew services start redis

# Start Celery worker
celery -A claude_goose worker --loglevel=info
```

## Usage Examples

### Using Gemini for Code Analysis

```python
from ai_integration.gemini_client import get_gemini_client

# Initialize client
gemini = get_gemini_client()

# Analyze code
code = """
def calculate_total(items):
    return sum([item['price'] for item in items])
"""

analysis = gemini.analyze_code(code, "Focus on Python best practices")
print(analysis)
```

### Using Claude for Code Generation (Headless Mode)

```python
from ai_integration.claude_client import get_claude_client

# Initialize client
claude = get_claude_client()

# Generate code
task = "Create a Django REST API endpoint for user registration"
result = claude.automate_code_task(task)
print(result)
```

### Using Background Tasks (Celery)

```python
from automation.tasks import analyze_codebase, automate_coding_task

# Queue a code analysis task
result = analyze_codebase.delay(your_code)
analysis = result.get()  # Wait for result

# Queue a coding task
task_result = automate_coding_task.delay(
    "Implement password reset functionality",
    codebase_context="Django REST API project"
)
code = task_result.get()
```

### Batch Processing Tasks

```python
from automation.tasks import batch_process_tasks

# Process multiple tasks (drip-feed to Claude)
tasks = [
    "Create user profile model",
    "Add profile API endpoints",
    "Implement profile image upload",
    "Add profile validation"
]

result = batch_process_tasks.delay(tasks)
results = result.get()  # Wait for all tasks to complete
```

## Admin Interface

Visit `http://localhost:8000/admin` and login with your superuser credentials to:
- Manage users
- View application logs
- Configure settings

## Optional: Tailscale Remote Configuration

To enable remote access via Tailscale:

1. Install Tailscale on your system
2. Update `.env`:
   ```bash
   TAILSCALE_ENABLED=True
   TAILSCALE_HOSTNAME=your-machine-name.tailnet-name.ts.net
   TAILSCALE_AUTH_KEY=your-tailscale-auth-key
   ```

## Testing the Installation

Run the installation test script:

```bash
python test_installation.py
```

## Troubleshooting

### "Module not found" errors
Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### Redis connection errors
Make sure Redis is installed and running:
```bash
redis-cli ping  # Should return "PONG"
```

### API key errors
Verify your API keys are correctly set in the `.env` file and are valid.

## Next Steps

1. **Explore the API**: Check out the REST API at `/api/`
2. **Read the Docs**: See `README.md` for detailed documentation
3. **Create Custom Tasks**: Add your own automation tasks in `automation/tasks.py`
4. **Integrate with CI/CD**: Use the automation features in your development workflow

## Support

- GitHub Issues: Report bugs and request features
- Documentation: Check `README.md` for detailed information
- Community: Share your automation workflows!

Happy coding! 🚀
