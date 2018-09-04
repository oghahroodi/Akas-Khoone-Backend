from json import dumps, loads

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class SearchTags(APIView):
    def post(self, request):
        tags = request.data['tags']
        tags = list(tags.split())
        query = Q()
        queryEq = Q()
        for entry in tags:
            query = query | Q(name__startswith=entry)
            queryEq = queryEq | Q(name=entry)
        q = Tag.objects.filter(query).order_by('-searchCount')
        qEq = Tag.objects.filter(queryEq)
        serializer = TagSerializers(q, many=True)
        serializerEq = TagSerializers(qEq, many=True)
        resultList = loads(dumps(serializer.data))[0:15]
        resultListEq = loads(dumps(serializerEq.data))
        resultFinalList = resultList + resultListEq
        resultFinalList = list({v['id']: v for v in resultFinalList}.values())
        result = {}
        j = 0
        for i in resultFinalList:
            j += 1
            result[j] = i

        return JsonResponse(result)


class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class GetTagsPosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = "tag"
    pagination_class = SetPagination

    def get_queryset(self, *args, **kwargs):

        t = self.kwargs.get(self.lookup_url_kwarg)
        tag = Tag.objects.get(name=t)
        tag.incrementSearchCount()
        tag.save()
        postIDs = TagPost.objects.filter(tag=tag.returnID())
        return Post.objects.filter(id__in=[i.returnPost() for i in postIDs])


class SearchUsers(APIView):
    def post(self, request):
        user = request.data['user']
        user = ''.join(user.split())
        query = Q()
        queryEq = Q()
        query = Q(username__startswith=user)
        queryEq = Q(username=user)
        q = Person.objects.filter(query).order_by('-followerNumber')
        qEq = Person.objects.filter(queryEq)
        serializer = PersonSerializer(q, many=True)
        serializerEq = PersonSerializer(qEq, many=True)
        resultList = loads(dumps(serializer.data))[0:1]
        resultListEq = loads(dumps(serializerEq.data))
        resultFinalList = resultListEq + resultList
        resultFinalList = list(
            {v['username']: v for v in resultFinalList}.values())
        result = {}
        j = 0
        for i in resultFinalList:
            j += 1
            result[j] = i

        return JsonResponse(result)
