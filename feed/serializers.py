from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "link",
            "author",
            "created",
            "votes",
        ]
        read_only_fields = ["author", "created", "votes"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "created"]
        read_only_fields = ["author", "created"]
