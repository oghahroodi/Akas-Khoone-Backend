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
import os
import binascii
import redis
import requests
import json
from Notification.producers import notif
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class GetID(APIView):
    def get(self, request):
        userid = request.user.
        logger.info(str(request.user.id)+" gets id")
        return JsonResponse({"id": userid})


class ProfileInfo(APIView):
    def get(self, request, pk):
        person = Person.objects.get(user__id=pk)
        serializer = PersonInfoSerializer(person,context={"userid": request.user.id})
        logger.info(str(request.user.id)+" :gets profile info")
        return JsonResponse(serializer.data)

    def patch(self, request, pk):
        userid = request.user.id
        if pk != userid:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        person = Person.objects.get(user__id=userid)
        serializer = PersonChangeInfoSerializer(
            person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(str(request.user.id)+" :change profile info")
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
            logger.info(str(request.user.id)+" :change password")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "رمز قدیمی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        registerdata = request.data.copy()
        userserializer = UserSerializer(
            data={"username": username, "password": password})
        if userserializer.is_valid():
            user = userserializer.save()
            userid = user.id
            user.set_password(password)
            user.is_active = False
            user.save()
            registerdata['user'] = userid
            personserializer = PersonSerializer(data=request.data)
            if personserializer.is_valid():
                person = personserializer.save()
                email(username)
                logger.info("user with email:"+username+"created")
                return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
            user.delete()
            return Response(personserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckUsername(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse({'status': 'پذیرفته شد'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckContacts(APIView):
    def post(self, request):
        emails = request.data.get("emails")
        contactSituation = []
        logger.info(str(request.user.id)+"see contact status")
        for email in emails:
            try:
                contact = User.objects.get(username=email["email"])
                email['id'] = contact.id
                email['username'] = Person.objects.get(
                    user_id=contact.id).username

                if contact.id != request.user.id:
                    try:
                        relation = Relation.objects.get(
                            userFollowing=request.user.id, userFollowed=contact.id)
                        email['status'] = contactState(0)
                    except Relation.DoesNotExist:
                        try:
                            req = FollowRequest.objects.get(
                                userFollowing=request.user.id, userFollowed=contact.id)
                            email['status'] = contactState(3)
                        except FollowRequest.DoesNotExist:
                            email['status'] = contactState(1)

            except User.DoesNotExist:
                email['status'] = contactState(2)
                email['id'] = -1
                email['username'] = ""

        return Response({"emails": emails}, status=status.HTTP_200_OK)


class Accept(APIView):

    def post(self, request, pk):
        try:
            contact = Person.objects.get(user_id=pk)
            if contact.user.id != self.request.user.id:
                try:

                    relation = Relation.objects.get(
                        userFollowed=request.user.id, userFollowing=contact.user.id)
                    return Response({"status": "شما را قبلا دنبال کرده."}, status=status.HTTP_200_OK)
                except Relation.DoesNotExist:

                    serializer = RelationSerializer(
                        data=makeRelation(contact.user.id, request.user.id))
                    try:
                        req = FollowRequest.objects.get(
                            userFollowed=request.user.id, userFollowing=contact.user.id)
                        if serializer.is_valid():
                            serializer.save()
                            req.delete()
                            followed = Person.objects.get(
                                user_id=request.user.id)
                            followed.incrementFollower()
                            followed.save()
                            follower = Person.objects.get(
                                user_id=contact.user.id)
                            follower.incrementFollowing()
                            follower.save
                            logger.info(str(request.user.id) +"accept"+str(pk)+"follow request")
                            return Response({"status": "به دنبال کننده های شما اضافه شد. "}, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    except FollowRequest.DoesNotExist:
                        return Response({"status": "شما از طرف این کاربر درخواست دنبال شدن ندارید."}, status=status.HTTP_404_NOT_FOUND)
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
        user = User.objects.get(id=self.kwargs.get('pk'))
        if (Relation.objects.filter(userFollowing_id=self.request.user.id, userFollowed_id=user.id)
                or self.kwargs.get('pk') == self.request.user.id):
            followers = Relation.objects.filter(userFollowed_id=self.kwargs.get('pk'))
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
        user = User.objects.get(id=self.kwargs.get('pk'))
        if (Relation.objects.filter(userFollowing_id=self.request.user.id, userFollowed_id=user.id)
                or self.kwargs.get('pk') == self.request.user.id):
            following = Relation.objects.filter(
                userFollowing_id=self.kwargs.get('pk'))
            if self.kwargs.get('searched') == "!":
                return Person.objects.filter(user_id__in=[i.followed() for i in following])
            else:

                return Person.objects.filter(user_id__in=[i.followed() for i in following],
                                             username__startswith=self.kwargs.get('searched'))
        else:
            return []


class Unfollow(APIView):
    def post(self, request):
        personUser = request.data.get("username")
        contact = Person.objects.get(username=personUser)
        try:

            relation = Relation.objects.get(
                userFollowing=request.user.id, userFollowed=contact.user.id)
            relation.delete()
            contact.decreseFollower()
            contact.save()
            person = Person.objects.get(user_id=request.user.id)
            person.decreseFollowing()
            person.save()
            logger.info(str(request.user.id) + "unfollow"+str(personUser))
            return Response({"status": "شما دیکر او را دنبال نمیکنید.","username":personUser}, status=status.HTTP_200_OK)
        except Relation.DoesNotExist:
            return Response({"status": "شما او را دنبال نمیکنید."}, status=status.HTTP_200_OK)


class ForgetPasswordEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(username=email)
            code = binascii.hexlify(os.urandom(2)).decode()
            emailPayload = makeMail(code)
            codeData = ForgetPassword(code=code, user=user)
            codeData.save()
            data = {"to": email, "body": emailPayload,
                    "subject": "فراموشی رمز عبور"}
            requests.post(url="http://192.168.10.66:80/api/send/mail", data=json.dumps(data),
                          headers={"agent-key": "OOmIZh9U6m", "content-type": "application/json"})
            logger.info("send forget pass email for email :"+email)
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
            FP = ForgetPassword.objects.get(user_id=user.id, code=token)
            if timezone.now()-FP.getDate() < timezone.timedelta(seconds=600):
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
        try:
            FP = ForgetPassword.objects.filter(user_id=user.id, accepted=True)
            user.set_password(newpassword)
            user.save()
            FP.delete()
            logger.info("user with eamil"+email+"change password")
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


class FriendInvite(APIView):
    def post(self, request):
        email = request.data.get('email')
        person = Person.objects.get(user_id=request.user.id)
        data = {"to": email, "body": person.name + "شمارا به نرم افزار عکاس خونه دعوت کرده است",
                "subject": "عکاس خونه"}

        requests.post(url="http://192.168.10.66:80/api/send/mail", data=json.dumps(data),
                      headers={"agent-key": "OOmIZh9U6m", "content-type": "application/json"})
        logger.info("user:"+str(request.user.id)+"invite friend :"+email)
        return Response({"status": "ایمیل با موفقیت ارسال شد."}, status=status.HTTP_200_OK)


class Follow(APIView):
    def post(self, request, pk):
        try:

            Person.objects.get(user_id=pk)
            if pk != self.request.user.id:
                try:

                    FollowRequest.objects.get(
                        userFollowing=request.user.id, userFollowed=pk)
                    return Response({"status": "شما قبلا درخواست دنبال کردن فرستاده اید."}, status=status.HTTP_200_OK)
                except FollowRequest.DoesNotExist:

                    serializer = FollowRequestSerializer(
                        data=makeRelation(request.user.id, pk))
                    if serializer.is_valid():
                        req=serializer.save()
                        
                        notif(kind='request', doer=request.user.id,
                              target=pk, date=req.date)
                        return Response({"status": "درخواست ارسال شد. ","userid":pk}, status=status.HTTP_201_CREATED)

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response({"status": "این کاربر وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)


class Reject(APIView):
    def post(self, request, pk):
        try:
            Person.objects.get(user_id=pk)
            try:
                req = FollowRequest.objects.get(
                    userFollowing=request.user.id, userFollowed=pk)
                req.delete()
                return Response({"status": "درخواست این کاربر رد شد."}, status=status.HTTP_200_OK)

            except FollowRequest.DoesNotExist:
                return Response({"status": "درخواست این کاربر قبلا رد شده است ."}, status=status.HTTP_404_NOT_FOUND)
        except Person.DoesNotExist:
            return Response({"status": "این کاربر وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)
