# text_similarity/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('select_folders/', views.select_folders, name='select_folders'),
    path('view_report/<int:report_id>/', views.view_report, name='view_report'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('download_report_csv/<int:report_id>/', views.download_report_csv, name='download_report_csv'),
    
]
