from django.urls import path

from db_manager import views

app_name = "db_manager"

urlpatterns = [
    path("db-manager", views.db_manager, name="db-manager"),
    path("documents-upload", views.documents_upload, name="documents-upload"),
    path("delete-data", views.delete_data, name="delete-data"),
]
