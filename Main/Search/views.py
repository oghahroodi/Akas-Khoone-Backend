from json import dumps, loads

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# class SearchTagsSuggestion(APIView):

#     def post(self, request):
#         tags = request.data['tags']
#         tags = list(tags.split())
#         data = {}

#         # Tag.objects.filter(Q(name__startswith= | )


#         # reqCount = 0
#         # for j in tags:
#         #     reqCount += 1
#         #     q = Tag.objects.all().filter(name__startswith=str(j))
#         #     serializer = TagSerializers(q, many=True)
#         #     resCount = 0
#         #     for i in loads(dumps(serializer.data)):
#         #         resCount+=1
#         #         data[str(reqCount) + "_" + str(resCount)] = i
#         return JsonResponse(data)


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
        postIDs = loads(dumps(TagPostSerializers(TagPost.objects.filter(
            tag=TagSerializers(Tag.objects.get(name=t)).data['id']), many=True).data))
        # ans = Post.objects.filter(id__in=[i['post'] for i in postIDs])
        # serializer = PostSerializer(ans, many=True)
        # result = {}
        # j = 0
        # for i in loads(dumps(serializer.data)):
        #     j+=1
        #     result[str(j)] = i
        # print (result)
        return Post.objects.filter(id__in=[i['post'] for i in postIDs])

        # +++++++++++++++++++++
        # query = Q()
        # for entry in postIDs:
        #     i = Post.objects.filter(id=entry['post'])
        #     query = query | Q(my_field__contains=entry)

        # queryset = MyModel.objects.filter(query)
        # +++++++++++++++++++++
