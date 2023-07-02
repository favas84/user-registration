from django.urls import path

from .views import (
    RegisterView, LoginView, StudentView, StaffView, AdminView, EditorView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('student/', StudentView.as_view(), name='student'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('admin/', AdminView.as_view(), name='admin'),
    path('editor/', EditorView.as_view(), name='editor'),
]
