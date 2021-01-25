from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoriesList, ProductViewSet, CommentCreate


router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('', include(router.urls)),
    path('comments/create/', CommentCreate.as_view()),
]
