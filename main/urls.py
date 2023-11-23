from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.UserInputRequestAPIView.as_view())
]
