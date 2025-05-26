from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),

    # Descent functionality
    path('start/', views.start_descent, name='start_descent'),
    path('journal/', views.journal_history, name='journal_history'),

    # Admin functionality
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Descent Type Management
    path('admin/descent-type/add/', views.descent_type_add, name='descent_type_add'),
    path('admin/descent-type/<int:pk>/edit/', views.descent_type_edit, name='descent_type_edit'),
    path('admin/descent-type/<int:pk>/delete/', views.descent_type_delete, name='descent_type_delete'),

    # Ritual Management
    path('admin/ritual/add/', views.ritual_add, name='ritual_add'),
    path('admin/ritual/<int:pk>/edit/', views.ritual_edit, name='ritual_edit'),
    path('admin/ritual/<int:pk>/delete/', views.ritual_delete, name='ritual_delete'),
]