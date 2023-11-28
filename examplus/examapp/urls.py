# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductAccessViewSet, CustomUserViewSet, LessonViewSet, LessonViewViewSet, UserLessonsViewSet, ProductLessonsViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'product-access', ProductAccessViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<str:product_id>/lessons',
         ProductViewSet.as_view({'get': 'list'})),
    path('product-access/<str:product_id>/users',
         ProductAccessViewSet.as_view({'get': 'list'})),
    path('users/<str:user_id>/lessons',
         CustomUserViewSet.as_view({'get': 'list'})),
    path('lessons/<str:lesson_id>/users',
         LessonViewSet.as_view({'get': 'list'})),
    path('lesson-views/<str:lesson_id>/users',
         LessonViewViewSet.as_view({'get': 'list'})),
    path('user-lessons/<str:user_id>/lessons',
         UserLessonsViewSet.as_view({'get': 'list'})),
    path('product-lessons/<str:product_id>/lessons',
         ProductLessonsViewSet.as_view({'get': 'list'})),



]
