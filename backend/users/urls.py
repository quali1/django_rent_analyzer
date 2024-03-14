from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path("profile/<int:pk>", views.user_profile, name="user-profile"),
    path('save-offer/<str:article_id>', views.save_offer, name="save-offer"),
    path('unsave-offer/<str:article_id>', views.unsave_offer, name="unsave-offer"),
]