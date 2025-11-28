from django.urls import path
from .views import delete_user

urlpatterns = [
    # other paths...
    path('delete_user/', delete_user, name='delete_user'),
]