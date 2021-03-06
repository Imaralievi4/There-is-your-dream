from rest_framework import serializers

from .models import Post, Categories, Comment
from account.models import User

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategoriesSerializer(instance.categories.all(), many=True).data
        representation['comments'] = CommentSerializer(instance.comment.all(), many=True).data
        return representation


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    
    class Meta:
        model = Post
        exclude = ('description', )

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategoriesSerializer(instance.categories.all(), many=True).data
        return representation


class CreateUpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description', 'price', 'categories')
