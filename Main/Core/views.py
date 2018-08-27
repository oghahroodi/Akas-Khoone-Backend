from rest_framework.views import APIView
from rest_framework import status
from .models import Person, Post, Relation
from .serializers import PersonSerializer, UserSerializer, PostSerializer, PersonUsernameSerializer, RelationSerializer
from .serializers import *
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import AllowAny
from .utilities import extractHashtags


class ProfileInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)

    def patch(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)


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


class CheckContacts(APIView):
    def post(self, request):
        personNumbers = request.data.get("PhoneNumbers");
        contactSituation=[]
        for Number in personNumbers:
            try:
                contact = Person.objects.get(phoneNumber=Number)
                try:
                    relation = Relation.objects.get(userFollowing=request.user.id, userFollower=contact.user.id)
                    contactSituation.append({'contact': PersonUsernameSerializer(contact).data,
                                             'status': contactState(0)})
                except Relation.DoesNotExist:
                    contactSituation.append({'contact': PersonUsernameSerializer(contact).data,
                                             'status': contactState(1)})

            except Person.DoesNotExist:
                contactSituation.append({'phoneNumber': Number, 'status': contactState(2)})
        return Response(contactSituation, status=status.HTTP_200_OK)

def contactState(index):
    if index == 0:
        return "friend"
    if index == 1:
        return "registered"
    if index == 2:
        return "notregistered"


class follow(APIView):
    def post(self, request):
        personUser = request.data.get("username");
        try:
            contact = Person.objects.get(username=personUser)
            try:
                relation = Relation.objects.get(userFollowing=request.user.id, userFollowed=contact.user.id)
                relation.delete()
                return Response({"status": "Unfollowed"}, status=status.HTTP_200_OK)
            except Relation.DoesNotExist:
                serializer = RelationSerializer(data=makeRelation(request.user.id, contact.user.id))
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status":"followed"}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            Response({"status": "user does not exist"}, status=status.HTTP_204_NO_CONTENT)


def makeRelation(following,followed):
    return {'userFollowing': following, 'userFollowed':followed}

