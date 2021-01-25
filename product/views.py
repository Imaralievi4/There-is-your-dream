from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as p, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .filters import ProductFilter
from .models import Product, Category, Comment
from .serializers import ProductSerializer, CategorySerializer, \
    CreateUpdateProductSerializer, CommentSerializer, ProductListSerializer


class MyPagination(PageNumberPagination):
    page_size = 5


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductSerializer
        elif self.action == 'list':
            return ProductListSerializer
        return CreateUpdateProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [p.IsAdminUser]
        return [permission() for permission in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                            Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreate(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
