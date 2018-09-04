from .serializer import *
from .models import *
from rest_framework import generics
from rest_framework.pagination import *




class SetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostComments(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('pk')).order_by('date')
