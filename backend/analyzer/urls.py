from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('analyzer/', views.analyzer_form, name='analyzer-form'),
    path('analysis/<str:request_id>', views.display_analysis, name='analysis'),
]
