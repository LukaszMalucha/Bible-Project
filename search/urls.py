from django.urls import path, include
from rest_framework.routers import DefaultRouter

from search import views

app_name = "search"

router = DefaultRouter()

router.register("search", views.BibleVerseViewSet, basename="search")

urlpatterns = [
    path("", include(router.urls)),
]