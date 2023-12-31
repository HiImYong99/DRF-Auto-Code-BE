from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.UserInputRequestAPIView.as_view()),
    path('response/', views.UserInputGetAPIView.as_view()),
    path('delete/<int:pk>/', views.UserInputDeleteAPIView.as_view()),
    path('delete/all/', views.UserInputDeleteAllAPIView.as_view()),
]
