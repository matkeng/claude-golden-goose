"""
REST API views for AI integration.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .gemini_client import get_gemini_client
from .claude_client import get_claude_client
from .tailscale_manager import get_tailscale_manager


@api_view(['GET'])
def status_view(request):
    """
    Get status of all AI integrations.
    """
    gemini = get_gemini_client()
    claude = get_claude_client()
    tailscale = get_tailscale_manager()
    
    return Response({
        'status': 'ok',
        'gemini': {
            'configured': bool(settings.GEMINI_API_KEY),
            'model': settings.GEMINI_MODEL,
            'initialized': gemini.model is not None,
        },
        'claude': {
            'configured': bool(settings.ANTHROPIC_API_KEY),
            'model': settings.CLAUDE_MODEL,
            'headless_mode': settings.CLAUDE_HEADLESS_MODE,
            'initialized': claude.client is not None,
        },
        'tailscale': tailscale.get_status() if tailscale else {'enabled': False},
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_code_view(request):
    """
    Analyze code using Gemini.
    
    POST /api/analyze-code/
    {
        "code": "def hello(): print('world')",
        "instructions": "Focus on code quality"
    }
    """
    code = request.data.get('code')
    instructions = request.data.get('instructions', '')
    
    if not code:
        return Response(
            {'error': 'Code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    gemini = get_gemini_client()
    if not gemini.model:
        return Response(
            {'error': 'Gemini not configured'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    analysis = gemini.analyze_code(code, instructions)
    
    return Response({
        'analysis': analysis,
        'model': settings.GEMINI_MODEL,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_tasks_view(request):
    """
    Generate task list from requirements using Gemini.
    
    POST /api/generate-tasks/
    {
        "requirements": "Build a user authentication system"
    }
    """
    requirements = request.data.get('requirements')
    
    if not requirements:
        return Response(
            {'error': 'Requirements are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    gemini = get_gemini_client()
    if not gemini.model:
        return Response(
            {'error': 'Gemini not configured'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    tasks = gemini.generate_tasks(requirements)
    
    return Response({
        'tasks': tasks,
        'model': settings.GEMINI_MODEL,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def automate_task_view(request):
    """
    Automate a coding task using Claude in headless mode.
    
    POST /api/automate-task/
    {
        "task": "Create a Django model for User Profile",
        "context": "Django project with PostgreSQL"
    }
    """
    task = request.data.get('task')
    context = request.data.get('context', '')
    
    if not task:
        return Response(
            {'error': 'Task description is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    claude = get_claude_client()
    if not claude.client:
        return Response(
            {'error': 'Claude not configured'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    result = claude.automate_code_task(task, context)
    
    return Response({
        'result': result,
        'model': settings.CLAUDE_MODEL,
        'headless_mode': settings.CLAUDE_HEADLESS_MODE,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_code_view(request):
    """
    Review code using Claude.
    
    POST /api/review-code/
    {
        "code": "def process_data(data): return data.sort()",
        "requirements": "Must handle edge cases"
    }
    """
    code = request.data.get('code')
    requirements = request.data.get('requirements', '')
    
    if not code:
        return Response(
            {'error': 'Code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    claude = get_claude_client()
    if not claude.client:
        return Response(
            {'error': 'Claude not configured'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    review = claude.review_code(code, requirements)
    
    return Response({
        'review': review,
        'model': settings.CLAUDE_MODEL,
    })
