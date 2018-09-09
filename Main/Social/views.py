from django.http.response import JsonResponse
from rest_framework.views import APIView

from .serializer import *
from .models import *
from rest_framework import generics, status
from rest_framework.pagination import *
from Notifications.producers import notif




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
        try:
            liked = Like.objects.get(user_id=request.user.id, post_id=pk)
            liked.delete()
            return JsonResponse({'status': 'دوست داشته نشد.'}, status=status.HTTP_200_OK)

        except Like.DoesNotExist:
            request.data['user'] = request.user.id
            request.data['post'] = pk
            serializer = LikeCreateSerializer(data=request.data)
            post = Post.objects.get(id=pk)
            post.increamentLike()
            post.save()
            userID = post.getUserID()
            notif('like', str(userID), p=str(pk))
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': "دوست داشته شد."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

