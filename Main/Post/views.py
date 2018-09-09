from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from Account.models import *
from Account.models import Person
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from  Social.models import Like

class PostDetails(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        if (Relation.objects.filter(userFollowed_id=post.getUserID(), userFollowing_id = request.user.id)
                or post.getUserID() == self.request.user.id):
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "شما اجازهی دست رسی به این صفحه را ندارید."}, status=status.HTTP_401_UNAUTHORIZED)


class SetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProfilePosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user.id
        return Post.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        tags = request.data.pop('tags')
        request.data['user'] = request.user.id
        person = Person.objects.get(user__id=request.user.id)
        request.data['profile'] = person.id
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            person.incrementPosts()
            tags = tags.split()
            # saving tags
            for t in tags:
                try:
                    tag = Tag.objects.get(name=t)
                except Tag.DoesNotExist:
                    tag = Tag(name=t)
                    tag.save()
                tagpost = TagPost(post=post, tag=tag)
                tagpost.save()

            return JsonResponse({'status': 'ساخته شد.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileBoards(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        userid = self.request.user.id
        return Board.objects.filter(user__id=userid)


class ProfileBoardPosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        board = Board.objects.get(id=pk)
        return board.posts.all().order_by('-date')


class HomePosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user.id
        postUsers = Relation.objects.filter(userFollowing_id=user)
        showableID=[]
        for i in postUsers:
            showableID.append(i.followed())
        showableID.append(user)
        homePosts = Post.objects.filter(user__in=[i for i in showableID]).order_by('-date')
        
        return homePosts

