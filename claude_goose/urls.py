"""
URL configuration for claude_goose project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from ai_integration import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/status/', api_views.status_view, name='api-status'),
    path('api/analyze-code/', api_views.analyze_code_view, name='analyze-code'),
    path('api/generate-tasks/', api_views.generate_tasks_view, name='generate-tasks'),
    path('api/automate-task/', api_views.automate_task_view, name='automate-task'),
    path('api/review-code/', api_views.review_code_view, name='review-code'),
    
    # REST Framework
    path('api-auth/', include('rest_framework.urls')),
]

# Debug toolbar (only in DEBUG mode)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
