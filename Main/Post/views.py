from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from .utilities import extractHashtags






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
        request.data['user'] = request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            tags = extractHashtags(request.data['description'])
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

