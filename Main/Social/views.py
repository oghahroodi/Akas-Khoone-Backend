from django.http.response import JsonResponse
from rest_framework.views import APIView

from .serializer import *
from .models import *
from rest_framework import generics, status
from rest_framework.pagination import *




class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostComments(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('pk')).order_by('date')


class Comment(APIView):
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = CommentCreateSerializer(data=request.data)
        post = Post.objects.get(id=request.data['post'])
        post.increamentComment()
        post.save()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'ساخته شد.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePosts(APIView):
    def post(self, request, pk):
        request.data['user'] = request.user.id
        request.data['post'] = pk
        serializer = LikeCreateSerializer(data=request.data)
        post = Post.objects.get()
        post.increamentLike()
        post.save()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'ساخته شد.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
