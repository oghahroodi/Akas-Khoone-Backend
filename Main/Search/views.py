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
        for entry in tags:
            query = query | Q(name__startswith=entry)

        q = Tag.objects.filter(query).order_by('-searchCount')
        serializer = TagSerializers(q, many=True)
        result = {}
        j = 0
        for i in loads(dumps(serializer.data))[0:15]:
            j += 1
            result[j] = i
        print(result)

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
