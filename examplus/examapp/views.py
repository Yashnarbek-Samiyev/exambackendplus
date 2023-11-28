from django.db.models import Sum, Count, Avg
from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import viewsets
from .models import Product, ProductAccess, Lesson, LessonView, CustomUser
from .serializers import ProductSerializer, ProductAccessSerializer, LessonSerializer, LessonViewSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(products__productaccess__user=user)


class LessonViewViewSet(viewsets.ModelViewSet):
    queryset = LessonView.objects.all()
    serializer_class = LessonViewSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAccessViewSet(viewsets.ModelViewSet):
    queryset = ProductAccess.objects.all()
    serializer_class = ProductAccessSerializer

# views.py


class UserLessonsViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(products__productaccess__user=user)


class ProductLessonsViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(products__id=product_id, products__productaccess__user=user)


class ProductStatistics(APIView):
    def get(self, request):
        products = Product.objects.all()
        stats = []
        for product in products:
            lessons_watched = LessonView.objects.filter(
                lesson__products=product).count()
            total_watching_time = LessonView.objects.filter(
                lesson__products=product).aggregate(Sum('viewing_time_seconds'))
            total_students = CustomUser.objects.filter(
                productaccess__product=product).count()
            product_access_percentage = ProductAccess.objects.filter(
                product=product).count() / CustomUser.objects.all().count() * 100

            stats.append({
                'product_name': product.name,
                'lessons_watched': lessons_watched,
                'total_watching_time': total_watching_time['viewing_time_seconds__sum'],
                'total_students': total_students,
                'product_access_percentage': product_access_percentage,
            })

        return Response(stats)
