import logging

from django.http import Http404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "post not found"


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def upvote(self, request, pk):
        try:
            post = self.get_object()
            post.votes += 1
            post.save()
            return Response({"votes": post.votes})
        except Http404:
            raise PostNotFound()
        except Exception as e:
            # possibly, overflow may happen,
            # but the error depends on db backend
            # so raising a generic error
            logging.error(e)
            raise APIException(detail="something went wrong")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # the code below is for demo purposes
    # it has been denied because it duplicates ViewSet functionality
    # so CommentViewSet is used instead
    # @action(detail=True, methods=["GET", "POST", "PUT", "DELETE"])
    # def comments(self, request, pk):
    #     if request.method == "GET":
    #         comments = Comment.objects.filter(post=pk)
    #         serializer = CommentSerializer(comments, many=True)
    #         return Response(serializer.data)

    #     elif request.method == "POST":
    #         serializer = CommentSerializer(data=request.data)
    #         if serializer.is_valid():
    #             post = self.get_object()
    #             serializer.save(post=post, author=request.user)
    #             return Response(
    #                 data=serializer.data, status=status.HTTP_201_CREATED
    #             )
    #         return Response(
    #             data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     elif request.method == "PUT":
    #         serializer = CommentSerializer(data=request.data)
    #         if serializer.is_valid():
    #             post = self.get_object()
    #             serializer.save(post=post, author=request.user)
    #             return Response(
    #                 data=serializer.data, status=status.HTTP_201_CREATED
    #             )
    #         return Response(
    #             data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     elif request.method == "DELETE":
    #         things are getting messy...


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get("post")
        try:
            post = Post.objects.get(pk=post_pk)
            return Comment.objects.filter(post=post)
        except Post.DoesNotExist as e:
            logging.error(e)
            raise PostNotFound()

    def perform_create(self, serializer):
        post_pk = self.kwargs.get("post")
        try:
            post = Post.objects.get(pk=post_pk)
            serializer.save(post=post, author=self.request.user)
        except Post.DoesNotExist as e:
            logging.error(e)
            raise PostNotFound()
