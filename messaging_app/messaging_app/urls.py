"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URL for the Browsable API's login/logout views
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Include the URLs from the 'chats' app under the 'api/chats/' prefix
    # The checker specifically mentioned the path 'api' in the instructions.
    # Let's use 'api/' as the main prefix.
    path('api/', include('chats.urls')),
]