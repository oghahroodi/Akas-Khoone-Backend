from json import dumps, loads

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.pagination import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)



class SearchTags(APIView):
    def post(self, request):
        tags = request.data['tags']
        tags = list(tags.split())
        tags = [i.lower() for i in tags]
        query = Q()
        queryEq = Q()
        for entry in tags:
            query = query | Q(name__startswith=entry)
            queryEq = queryEq | Q(name=entry)
        q = Tag.objects.filter(query).order_by('-searchCount')
        qEq = Tag.objects.filter(queryEq)
        serializer = TagSerializers(q, many=True, context={
                                    "userid": request.user.id})
        serializerEq = TagSerializers(qEq, many=True, context={
                                      "userid": request.user.id})
        resultList = loads(dumps(serializer.data))[0:15]
        resultListEq = loads(dumps(serializerEq.data))
        resultFinalList = resultList + resultListEq
        resultFinalList = list({v['id']: v for v in resultFinalList}.values())
        result = {"results": resultFinalList}
        logger.info("user:"+str(request.user.id) +"search for"+request.data['tags'])

        return JsonResponse(result, status=status.HTTP_200_OK)


class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class GetTagsPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = "tag"
    pagination_class = SetPagination

    def get_queryset(self, *args, **kwargs):

        t = self.kwargs.get(self.lookup_url_kwarg)
        tag = Tag.objects.get(name=t)
        tag.incrementSearchCount()
        tag.save()

        userid = self.request.user.id
        allowedUser = Relation.objects.filter(userFollowing_id=userid)

        postIDs = TagPost.objects.filter(tag=tag.returnID())
        allowed = [i.followed() for i in allowedUser]
        allowed.append(userid)
        logger.info("user:"+str(self.request.user.id) + "click on"+t)
        return Post.objects.filter(id__in=[i.returnPost() for i in postIDs], user_id__in=allowed)


class SearchUsers(APIView):
    def post(self, request):
        user = request.data['user']
        user = ''.join(user.split())
        query = Q(username__startswith=user) | Q(name__startswith=user)
        queryEq = Q(username=user) | Q(name=user)
        q = Person.objects.filter(query).order_by('-followerNumber')
        qEq = Person.objects.filter(queryEq)
        serializer = PersonSerializer(q, many=True, context={"userid": request.user.id})
        serializerEq = PersonSerializer(qEq, many=True, context={"userid": request.user.id})
        resultList = loads(dumps(serializer.data))[0:15]
        resultListEq = loads(dumps(serializerEq.data))
        resultFinalList = resultListEq + resultList
        resultFinalList = list(
            {v['username']: v for v in resultFinalList}.values())
        result = {"results": resultFinalList}
        logger.info("user:"+str(request.user.id) +"search for"+request.data['user'])
        return JsonResponse(result, status=status.HTTP_200_OK)


class TrendingTags(APIView):
    def get(self, request):
        q = Tag.objects.all().order_by('-searchCount')
        serializer = TagSerializers(q, many=True)
        resultList = loads(dumps(serializer.data))[0:15]
        result = {"results": resultList}

        return JsonResponse(result, status=status.HTTP_200_OK)
