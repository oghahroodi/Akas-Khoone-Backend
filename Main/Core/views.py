from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from Core.models import Person, Post
from Core.serializers import PersonSerializer,PostSerializer
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import *

class SendInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)

class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class SendPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user.id
        return Post.objects.filter(person=user)