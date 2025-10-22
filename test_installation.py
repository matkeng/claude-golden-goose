#!/usr/bin/env python
"""
Test script to verify Claude Golden Goose installation and configuration.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claude_goose.settings')
django.setup()

from django.conf import settings
from ai_integration.gemini_client import GeminiClient
from ai_integration.claude_client import ClaudeClient
from ai_integration.tailscale_manager import TailscaleManager


def test_django_config():
    """Test Django configuration."""
    print("\n=== Django Configuration ===")
    print(f"✓ Django version: {django.get_version()}")
    print(f"✓ Debug mode: {settings.DEBUG}")
    print(f"✓ Secret key configured: {bool(settings.SECRET_KEY)}")
    print(f"✓ Allowed hosts: {settings.ALLOWED_HOSTS}")
    print(f"✓ Database: {settings.DATABASES['default']['ENGINE']}")
    return True


def test_gemini_config():
    """Test Gemini configuration."""
    print("\n=== Google Gemini Configuration ===")
    api_key = settings.GEMINI_API_KEY
    model = settings.GEMINI_MODEL
    
    if api_key:
        print(f"✓ API key configured (length: {len(api_key)})")
        print(f"✓ Model: {model}")
        
        # Try to initialize client
        try:
            client = GeminiClient()
            if client.model:
                print("✓ Gemini client initialized successfully")
            else:
                print("⚠ Gemini client initialized but model not loaded (check API key)")
            return True
        except Exception as e:
            print(f"✗ Error initializing Gemini client: {e}")
            return False
    else:
        print("⚠ Gemini API key not configured in .env file")
        print("  Add GEMINI_API_KEY to .env to enable Gemini integration")
        return True  # Not a failure, just not configured


def test_claude_config():
    """Test Claude configuration."""
    print("\n=== Claude (Anthropic) Configuration ===")
    api_key = settings.ANTHROPIC_API_KEY
    model = settings.CLAUDE_MODEL
    headless = settings.CLAUDE_HEADLESS_MODE
    
    if api_key:
        print(f"✓ API key configured (length: {len(api_key)})")
        print(f"✓ Model: {model}")
        print(f"✓ Headless mode: {headless}")
        
        # Try to initialize client
        try:
            client = ClaudeClient()
            if client.client:
                print("✓ Claude client initialized successfully")
            else:
                print("⚠ Claude client initialized but not connected (check API key)")
            return True
        except Exception as e:
            print(f"✗ Error initializing Claude client: {e}")
            return False
    else:
        print("⚠ Anthropic API key not configured in .env file")
        print("  Add ANTHROPIC_API_KEY to .env to enable Claude integration")
        return True  # Not a failure, just not configured


def test_tailscale_config():
    """Test Tailscale configuration."""
    print("\n=== Tailscale Configuration ===")
    enabled = settings.TAILSCALE_ENABLED
    
    if enabled:
        print(f"✓ Tailscale enabled")
        print(f"✓ Hostname: {settings.TAILSCALE_HOSTNAME}")
        
        try:
            manager = TailscaleManager()
            status = manager.get_status()
            print(f"✓ Tailscale manager initialized")
            print(f"  Connected: {status['connected']}")
            return True
        except Exception as e:
            print(f"✗ Error initializing Tailscale manager: {e}")
            return False
    else:
        print("⚠ Tailscale not enabled")
        print("  Set TAILSCALE_ENABLED=True in .env to enable Tailscale")
        return True


def test_celery_config():
    """Test Celery configuration."""
    print("\n=== Celery Configuration ===")
    print(f"✓ Broker URL: {settings.CELERY_BROKER_URL}")
    print(f"✓ Result backend: {settings.CELERY_RESULT_BACKEND}")
    print(f"✓ Task serializer: {settings.CELERY_TASK_SERIALIZER}")
    
    # Note: We can't test actual Redis connection without Redis running
    print("\n  Note: To test Celery, ensure Redis is running and execute:")
    print("    celery -A claude_goose worker --loglevel=info")
    return True


def test_installed_apps():
    """Test installed apps."""
    print("\n=== Installed Applications ===")
    required_apps = [
        'rest_framework',
        'corsheaders',
        'debug_toolbar',
        'ai_integration',
        'automation',
    ]
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"✓ {app}")
        else:
            print(f"✗ {app} not installed")
            return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Claude Golden Goose - Installation Verification")
    print("=" * 60)
    
    tests = [
        ("Django Configuration", test_django_config),
        ("Gemini Configuration", test_gemini_config),
        ("Claude Configuration", test_claude_config),
        ("Tailscale Configuration", test_tailscale_config),
        ("Celery Configuration", test_celery_config),
        ("Installed Apps", test_installed_apps),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error running {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! The installation is complete.")
        print("\nNext steps:")
        print("1. Configure API keys in .env file")
        print("2. Run 'python manage.py createsuperuser' to create an admin user")
        print("3. Run 'python manage.py runserver' to start the development server")
        print("4. Visit http://localhost:8000/admin to access the admin panel")
        return 0
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
