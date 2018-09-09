from rest_framework.views import APIView
from rest_framework import status, generics
from .serializers import *
from django.http import JsonResponse
from rest_framework.pagination import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .utilities import *
from rest_framework.permissions import AllowAny


class GetID(APIView):
    def get(self, request):
        userid = request.user.id
        return JsonResponse({"id": userid})


class ProfileInfo(APIView):
    def get(self, request, pk):
        person = Person.objects.get(user__id=pk)
        serializer = PersonInfoSerializer(person)
        return JsonResponse(serializer.data)

    def patch(self, request, pk):
        userid = request.user.id
        if pk != userid:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        person = Person.objects.get(user__id=userid)
        serializer = PersonChangeInfoSerializer(person, data=request.data, partial=True)
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


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data.get('user')['username'])
            user.set_password(request.data.get('user')['password'])
            user.save()
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
        contactSituation = []
        for Number in personNumbers:
            try:
                contact = Person.objects.get(phoneNumber=Number)
                try:
                    relation = Relation.objects.get(userFollowing=request.user.id, userFollowed=contact.user.id)
                    contactSituation.append({'contact': PersonFollowPageSerializer(contact).data,
                                             'status': contactState(0)})
                except Relation.DoesNotExist:
                    contactSituation.append({'contact': PersonFollowPageSerializer(contact).data,
                                             'status': contactState(1)})

            except Person.DoesNotExist:
                contactSituation.append({'phoneNumber': Number, 'status': contactState(2)})
        return Response(contactSituation, status=status.HTTP_200_OK)


class Accept(APIView):

    def post(self, request):

        personUser = request.data.get("username");
        try:

            contact = Person.objects.get(username=personUser)
            if contact.user.id!=self.request.user.id:
                try:

                    relation = Relation.objects.get(userFollowed=request.user.id, userFollowing=contact.user.id)
                    return Response({"status": "already accepted"}, status=status.HTTP_200_OK)
                except Relation.DoesNotExist:


                    serializer = RelationSerializer(data=makeRelation(contact.user.id, request.user.id))
                    if serializer.is_valid():
                        serializer.save()
                        followed = Person.objects.get(user_id=request.user.id)
                        followed.incrementFollower()
                        followed.save()
                        follower = Person.objects.get(user_id=contact.user.id)
                        follower.incrementFollowing()
                        follower.save()
                        return Response({"status": "followed"}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except Person.DoesNotExist:
            return Response({"status": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)


class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class Followers(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = Person.objects.get(user_id=self.kwargs.get('pk'))
        if (Relation.objects.filter(userFollowing_id=self.request.user.id, userFollowed_id=user.getID())
                or self.kwargs.get('pk') == self.request.user.id):
            followers = Relation.objects.filter(userFollowed_id=self.request.user.id)
            print(followers)
            if self.kwargs.get('searched') == "!":
                return Person.objects.filter(user_id__in=[i.following() for i in followers])
            else:

                return Person.objects.filter(user_id__in=[i.following() for i in followers],
                                             username__startswith=self.kwargs.get('searched'))
        else:
            return []


class Followings(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = Person.objects.get(user_id=self.kwargs.get('pk'))
        if (Relation.objects.filter(userFollowing_id=self.request.user.id, userFollowed_id=user.getID())
                or self.kwargs.get('pk') == self.request.user.id):
            following = Relation.objects.filter(userFollowing_id=self.request.user.id)
            if self.kwargs.get('searched') == "!":
                return Person.objects.filter(user_id__in=[i.followed() for i in following])
            else:

                return Person.objects.filter(user_id__in=[i.followed() for i in following],
                                             username__startswith=self.kwargs.get('searched'))
        else:
            return []
