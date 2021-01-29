from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as p, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import PostFilter
from .models import Post, Categories, Comment
from .serializers import PostSerializer, CategoriesSerializer, \
    CreateUpdatePostSerializer, CommentsSerializer, PostListSerializer


class MyPagination(PageNumberPagination):
    page_size = 5


class CategoriesList(ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostSerializer
        elif self.action == 'list':
            return PostListSerializer
        return CreateUpdatePostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [p.IsAuthenticated]
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                            Q(description__icontains=q))
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreate(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
