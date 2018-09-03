from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from Account.models import *
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from .utilities import extractHashtags


class PostDetails(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        if (Relation.objects.filter(userFollowed_id=post.getUserID(), userFollowing_id= request.user.id)):
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            Response({"status": "Not_Authorized"}, status=status.HTTP_400_BAD_REQUEST)


class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProfilePosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user.id
        return Post.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        tags = request.data.pop('tags')
        request.data['user'] = request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            for t in tags:
                try:
                    tag = Tag.objects.get(name=t)
                except Tag.DoesNotExist:
                    tag = Tag(name=t)
                    tag.save()
                tagpost = TagPost(post=post, tag=tag)
                tagpost.save()
                return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomePosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user.id
        postUsers = Relation.objects.filter(userFollowing_id=user)
        return Post.objects.filter(user__in=[i.followed()for i in postUsers]).order_by('date')

