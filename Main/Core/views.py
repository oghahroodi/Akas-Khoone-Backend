from rest_framework.views import APIView
from rest_framework import status
from Core.models import Person, Post
from Core.serializers import PersonSerializer,PostSerializer
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import *
from rest_framework.parsers import JSONParser

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


class SendContactPerson(APIView):

    def post(self, request):
        responseJSON = {}
        phoneList = request.data["phoneNumber"].split(',')
        for i in phoneList:
            pass

        return Response({'received data': request.data})



