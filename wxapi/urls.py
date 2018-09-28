from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('login/<str:appid>/', views.login),
    path('access_token/<str:appid>/', views.get_access_token),
    path('posts/', views.get_post_titles),
    path('posts/<int:post_id>/', views.get_post_detail),
    path('comments/<int:post_id>/', views.get_post_comment),
    path('comments/<int:post_id>/add/', views.add_comment),
]
