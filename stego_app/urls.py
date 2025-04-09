from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('image_steg/', views.image_steg, name='image_steg'),
    path('video_steg/', views.video_steg, name='video_steg'),
    path('audio_steg/', views.audio_steg, name='audio_steg'),
]
