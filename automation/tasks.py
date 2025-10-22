"""
Celery tasks for automation.
"""
import logging
from celery import shared_task
from ai_integration.gemini_client import get_gemini_client
from ai_integration.claude_client import get_claude_client

logger = logging.getLogger(__name__)


@shared_task
def analyze_codebase(code_content, instructions=""):
    """
    Analyze codebase using Gemini.
    
    Args:
        code_content: Code to analyze
        instructions: Optional specific instructions
        
    Returns:
        Analysis results
    """
    logger.info("Starting codebase analysis task")
    gemini = get_gemini_client()
    result = gemini.analyze_code(code_content, instructions)
    logger.info("Codebase analysis completed")
    return result


@shared_task
def generate_task_list(requirements):
    """
    Generate task list from requirements using Gemini.
    
    Args:
        requirements: Project requirements
        
    Returns:
        Generated task list
    """
    logger.info("Generating task list")
    gemini = get_gemini_client()
    result = gemini.generate_tasks(requirements)
    logger.info("Task list generated")
    return result


@shared_task
def automate_coding_task(task_description, codebase_context=""):
    """
    Automate a coding task using Claude in headless mode.
    
    Args:
        task_description: Description of the task
        codebase_context: Context about the codebase
        
    Returns:
        Generated code/solution
    """
    logger.info(f"Starting automated coding task: {task_description[:50]}...")
    claude = get_claude_client()
    result = claude.automate_code_task(task_description, codebase_context)
    logger.info("Coding task completed")
    return result


@shared_task
def review_code_changes(code, requirements=""):
    """
    Review code changes using Claude.
    
    Args:
        code: Code to review
        requirements: Optional requirements
        
    Returns:
        Review feedback
    """
    logger.info("Starting code review")
    claude = get_claude_client()
    result = claude.review_code(code, requirements)
    logger.info("Code review completed")
    return result


@shared_task
def create_improvement_plan(codebase_analysis):
    """
    Create improvement plan using Claude.
    
    Args:
        codebase_analysis: Analysis of the codebase
        
    Returns:
        Improvement plan
    """
    logger.info("Creating improvement plan")
    claude = get_claude_client()
    result = claude.generate_improvement_plan(codebase_analysis)
    logger.info("Improvement plan created")
    return result


@shared_task
def batch_process_tasks(task_list):
    """
    Process multiple coding tasks in batch (drip-feed to Claude).
    
    Args:
        task_list: List of task descriptions
        
    Returns:
        List of results
    """
    logger.info(f"Starting batch processing of {len(task_list)} tasks")
    results = []
    
    for i, task in enumerate(task_list, 1):
        logger.info(f"Processing task {i}/{len(task_list)}")
        result = automate_coding_task.apply(args=[task])
        results.append(result.get())
    
    logger.info("Batch processing completed")
    return results
