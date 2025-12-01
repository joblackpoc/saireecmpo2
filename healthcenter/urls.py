from django.urls import path
from . import views

app_name = 'healthcenter'

urlpatterns = [
    path('', views.home, name='home'),

    # About CRUD URLs
    path('about/', views.AboutListView.as_view(), name='about_list'),
    path('about/<int:pk>/', views.AboutDetailView.as_view(), name='about_detail'),
    path('about/create/', views.AboutCreateView.as_view(), name='about_create'),
    path('about/<int:pk>/update/', views.AboutUpdateView.as_view(), name='about_update'),
    path('about/<int:pk>/delete/', views.AboutDeleteView.as_view(), name='about_delete'),

    path('homepage/create/', views.HomeCreateView.as_view(), name='home_create'),

    path('portfolio/create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio/', views.PortfolioListView.as_view(), name='portfolio_list'),
    path('portfolio/<int:pk>/update/', views.PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('portfolio/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('portfolio/<int:pk>/delete/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'),
    # Content CRUD URLs
    path('content/', views.content, name='content'),
    path('content/create/', views.ContentCreateView.as_view(), name='content_create'),
    path('content/<int:pk>/update/', views.ContentUpdateView.as_view(), name='content_update'),
    path('content/<int:pk>/delete/', views.ContentDeleteView.as_view(), name='content_delete'),
]