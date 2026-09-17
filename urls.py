from django.urls import path
from . import views

urlpatterns = [
    # Template UI Routes
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('donors/', views.donor_list_view, name='donor_list'),
    path('donors/add/', views.donor_add_view, name='donor_add'),
    path('donors/<int:pk>/', views.donor_detail_view, name='donor_detail'),
    path('donors/<int:pk>/edit/', views.donor_edit_view, name='donor_edit'),
    path('donors/<int:pk>/delete/', views.donor_delete_view, name='donor_delete'),
    path('about/', views.about_view, name='about'),

    # REST API Routes (DRF)
    path('api/donors/', views.DonorListCreateAPIView.as_view(), name='api_donor_list_create'),
    path('api/donors/<int:pk>/', views.DonorDetailAPIView.as_view(), name='api_donor_detail'),
    path('api/statistics/', views.StatisticsAPIView.as_view(), name='api_statistics'),
]
