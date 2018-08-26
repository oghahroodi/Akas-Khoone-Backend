from rest_framework.views import APIView
from rest_framework import status
from Core.models import Person, Post
from Core.serializers import PersonSerializer, UserSerializer, PostSerializer
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from rest_framework.permissions import AllowAny


class ProfileInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)


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
        return Post.objects.filter(person=user)

    #def post(self, request, *args, **kwargs):
    #    userid = request.user.id
    #    person = Person.objects.get(user__id=userid)



class SendContactPerson(APIView):

    def post(self, request):
        responseJSON = {}
        phoneList = request.data["phoneNumber"].split(',')
        for i in phoneList:
            pass

        return Response({'received data': request.data})


class CreateUser(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckUsername(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse({'status': 'ACCEPTED'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)