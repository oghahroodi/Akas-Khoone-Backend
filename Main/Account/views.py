from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework import status, generics
from .serializers import *
from django.http import JsonResponse
from rest_framework.pagination import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .utilities import *
from rest_framework.permissions import AllowAny
import os, binascii, redis, requests, json


class ProfileInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonInfoSerializer(person)
        return JsonResponse(serializer.data)

    def patch(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonChangeInfoSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OthersProfileInfo(APIView):
    def get(self, request, pk):
        userid = request.user.id
        try:
            Relation.objects.get(userFollowed=pk, userFollowing=userid)
            person = Person.objects.get(user__id=pk)
            serializer = PersonInfoSerializer(person)
            return JsonResponse(serializer.data)
        except Relation.DoesNotExist:
            return JsonResponse({"status": "شما اجازهی دست رسی به این صفحه را ندارید."},
                                status=status.HTTP_401_UNAUTHORIZED)


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
        return Response({"status": "رمز قدیمی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.pop('email')[0]
        password = request.data.pop('password')[0]
        userserializer = UserSerializer(data={"username": username, "password": password} )
        if userserializer.is_valid():
            user = userserializer.save()
            userid = user.id
            user.set_password(password)
            user.is_active = False
            user.save()
            request.data['user'] = userid
            personserializer = PersonSerializer(data=request.data)
            if personserializer.is_valid():
                person = personserializer.save()
                email(username)
                return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
            user.delete()
            return Response(personserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # serializer = PersonSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     username = request.data.get('user')['username']
        #     user = User.objects.get(
        #         username=username)
        #     user.set_password(request.data.get('user')['password'])
        #     user.is_active = False
        #     user.save()
        #     email(username)
        #     return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckUsername(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse({'status': 'پذیرفته شد'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckContacts(APIView):
    def post(self, request):
        personNumbers = request.data.get("PhoneNumbers")
        contactSituation = []
        for Number in personNumbers:
            try:
                contact = Person.objects.get(phoneNumber=Number)
                try:
                    relation = Relation.objects.get(
                        userFollowing=request.user.id, userFollowed=contact.user.id)
                    contactSituation.append({'contact': PersonFollowPageSerializer(contact).data,
                                             'status': contactState(0)})
                except Relation.DoesNotExist:
                    contactSituation.append({'contact': PersonFollowPageSerializer(contact).data,
                                             'status': contactState(1)})

            except Person.DoesNotExist:
                contactSituation.append(
                    {'phoneNumber': Number, 'status': contactState(2)})
        return Response(contactSituation, status=status.HTTP_200_OK)


class Accept(APIView):

    def post(self, request):

        personUser = request.data.get("username");
        try:

            contact = Person.objects.get(username=personUser)
            if contact.user.id != self.request.user.id:
                try:

                    relation = Relation.objects.get(userFollowed=request.user.id, userFollowing=contact.user.id)
                    return Response({"status": "شما را قبلا دنبال کرده."}, status=status.HTTP_200_OK)
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
                        return Response({"status": "به دنبال کننده های شما اضافه شد. "}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except Person.DoesNotExist:
            return Response({"status": "این کاربر وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)


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


class Unfollow(APIView):
    def post(self, request):
        personUser = request.data.get("username");
        contact = Person.objects.get(username=personUser)
        try:

            relation = Relation.objects.get(userFollowing=request.user.id, userFollowed = contact.user.id)
            relation.delete()
            return Response({"status": "شما دیکر او را دنبال نمیکنید."}, status=status.HTTP_200_OK)
        except Relation.DoesNotExist:
            return Response({"status": "شما او را دنبال نمیکنید."}, status=status.HTTP_200_OK)


class ForgetPasswordEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(username=email)
            code = binascii.hexlify(os.urandom(5)).decode()
            emailPayload = makeMail(code)
            codeData = ForgetPassword(code=code, user=user)
            codeData.save()
            data = {"to": email, "body": emailPayload, "subject": "فراموشی رمز عبور"}
            requests.post(url="http://192.168.10.66:80/api/send/mail", data=json.dumps(data),
                          headers={"agent-key": "OOmIZh9U6m", "content-type": "application/json"})
            return Response({"status": "ایمیل با موفقیت ارسال شد."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"status": "این کاربر وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)


class ForgetPasswordTokenCheck(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        user = User.objects.get(username=email)
        try:
            FP = ForgetPassword.objects.get(user_id=user.id,code=token)
            if FP.getDate()-timezone.now() < timezone.datetime(minute=20):
                FP.accept()
                return Response({"status": "تایید شد."}, status=status.HTTP_200_OK)

            else:
                FP.delete()
                return Response({"status": "زمان کد پایان یافته."}, status=status.HTTP_406_NOT_ACCEPTABLE)


        except ForgetPassword.DoesNotExist:
            return Response({"status": "کد نامعتبر."}, status=status.HTTP_404_NOT_FOUND)

class ForgetPasswordNewPassword(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(username=email)
        newpassword = request.data.get('password')
        try :
            FP=ForgetPassword.objects.filter(user_id=user.id, accepted=True)
            user.set_password(newpassword)
            user.save()
            FP.delete()
            return Response({"status": "رمز شما تغییر کرد."}, status=status.HTTP_200_OK)

        except ForgetPassword.DoesNotExist:
            return Response({"status": "درخواست نا معتبر."}, status=status.HTTP_404_NOT_FOUND)


def validation(request, token):
    red = redis.StrictRedis(host='localhost', port=6379,
                            password='', charset="utf-8", decode_responses=True)
    info = red.hgetall(token)
    email = info.get('email')
    if not (info and email):
        print("PermissionDenied")

    user = User.objects.get(username=email)
    user.is_active = True
    user.save()
    return HttpResponse()
