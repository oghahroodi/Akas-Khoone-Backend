
from json import dumps, loads

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
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
        #print(resultFinalList)
        result = {"results": resultFinalList}
        # j = 0
        # for i in resultFinalList:
        #     j += 1
        #     result[j] = i

        return JsonResponse(result, status=status.HTTP_200_OK)

