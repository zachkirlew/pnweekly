from rest_framework import serializers
from users.models import CustomUser
from articles.models import Article, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','id')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id','article', 'user', 'text', 'created_date')


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name')


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    source_name = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=300)
    description = serializers.CharField()
    image_url = serializers.CharField()
    published_at = serializers.DateTimeField()
    likes = LikeSerializer(required=False, many=True)

    class Meta:
        model = Article
        fields = ('id', 'source_name', 'author', 'title', 'description', 'title', 'image_url', 'published_at', 'likes')
