from rest_framework.views import APIView
from rest_framework import status
from .models import Person, Post
from .serializers import UserSerializer, PersonSerializer, PostSerializer
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import AllowAny



class sendInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)




class ChangePassword(APIView):
    def patch(self, request):
        old = request.data.get("oldPassword")
        new = request.data.get("newPassword")
        validate_password(new)
        if request.user.check_password(old):
            user = User.objects.get(id=request.user.id)
            user.set_password(new)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)


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
        return Post.objects.filter(user=user)


class SendContactPerson(APIView):
    pass

    # def post(self, request):
    #     responseJSON = {}
    #     phoneList = request.data["phoneNumber"].split(',')
    #     for i in phoneList:
    #         pass

    #     return Response({'received data': request.data})



class CreateUser(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckUsername(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse({'status': 'ACCEPTED'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakePost(APIView):

    def post(self, request):
        userid = request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
