from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('access_token/<str:appid>/', views.get_access_token),
    path('posts/', views.get_post_titles),
    path('posts/<int:post_id>/', views.get_post_detail),
]
