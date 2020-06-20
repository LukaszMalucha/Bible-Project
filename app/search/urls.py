from django.urls import path, include
from rest_framework.routers import DefaultRouter

from search import views

app_name = "search"

router = DefaultRouter()

router.register("search", views.BibleVerseViewSet, basename="search")

urlpatterns = [
    path("", include(router.urls)),
    path("keyword/<str:keyword>", views.KeywordSearch.as_view(), name="keyword"),
    path("book/<str:book>", views.BookSearch.as_view(), name="book"),
]