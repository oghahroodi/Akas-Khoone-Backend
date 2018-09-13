from django.http import JsonResponse
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import NotifSerializer
from rest_framework.pagination import *
from .models import *
from Post.models import *
from rest_framework import generics


class SetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class getNotification(generics.ListAPIView):
    queryset = Notif.objects.all()
    serializer_class = NotifSerializer
    pagination_class = SetPagination

    def get_queryset(self, *args, **kwargs):

        try:
            return Notif.objects.filter(user=str(self.request.user.id))
        except Notif.DoesNotExist:
            return[]


class Notification(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        if request.META.get("REMOTE_ADDR") == "127.0.0.1":
            kind = request.POST['kind']
            doer = request.POST['doer']
            # print(kind)
            # print(doer)
            if kind == "comment" or kind == "like":
                entity = request.POST['entity']
                # print(entity)
            if kind == "request":
                target = request.POST['target']
                # print(target)
            date = request.POST['date']

            if kind == 'comment' or kind == 'like':
                post = Post.objects.all().filter(pk=int(entity)).first()
                user = User.objects.all().filter(id=doer).first()

                n = Notif.objects.filter(user=str(post.user.id), entity=post)
                if n.count() == 0:
                    if (str(post.user.id) != str(user.id)):
                        notif = Notif(kind=kind, entity=post, doer=user.person,
                                      date=date, user=str(post.user.id))
                        notif.save()
            if kind == "request":
                user = User.objects.all().filter(id=doer).first()
                notif = Notif(kind=kind, date=date,
                              doer=user.person, user=target)
                notif.save()

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
