from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from Account.models import *
from Account.serializers import PersonSerializer
from Account.models import Person
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import *
from  Social.models import Like
from .utilities import extractHashtags
from Notifications.producers import notif


class PostDetails(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        if (Relation.objects.filter(userFollowed_id=post.getUserID(), userFollowing_id=request.user.id)
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

    def get(self, request, *args, **kwargs):
        userid = self.request.user.id
        pk = self.kwargs.get('pk')
        try:
            if pk != userid:
                Relation.objects.get(userFollowed=pk, userFollowing=userid)
            return self.list(request, *args, **kwargs)
        except Relation.DoesNotExist:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        userid = self.request.user.id
        pk = self.kwargs.get('pk')
        if pk != userid:
            return Response({"status": "شما اجازهی دست رسی به این صفحه را ندارید."}, status=status.HTTP_401_UNAUTHORIZED)
        tags = request.data.pop('tags')[0]
        request.data['user'] = userid
        person = Person.objects.get(user__id=request.user.id)
        request.data['profile'] = person.id
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            person.incrementPosts()
            person.save()
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
            # notif('post', request.user.id, serializer.id)
            return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileBoards(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    pagination_class = SetPagination

    def get_serializer_context(self):
        return {'pk': self.request.user.id}

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Board.objects.filter(user__id=pk)

    def get(self, request, *args, **kwargs):
        userid = self.request.user.id
        pk = self.kwargs.get('pk')
        try:
            if pk != userid:
                Relation.objects.get(userFollowed=pk, userFollowing=userid)
            return self.list(request, *args, **kwargs)
        except Relation.DoesNotExist:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        userid = self.request.user.id
        pk = self.kwargs.get('pk')
        if pk != userid:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        request.data['user'] = userid
        serializer = CreateBoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetails(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        board = Board.objects.get(id=pk)
        return board.posts.all().order_by('-date')
        userid = self.request.user.id
        boardid = self.kwargs.get('boardid')
        board = Board.objects.get(id=boardid)
        usersAllowed = [i.followed() for i in Relation.objects.filter(userFollowing__id=userid)]
        usersAllowed.append(userid)
        return board.posts.filter(user__in=usersAllowed)

    def get(self, request, *args, **kwargs):
        userid = self.request.user.id
        boardid = self.kwargs.get('boardid')
        pk = Board.objects.get(id=boardid).user.id
        try:
            if pk != userid:
                Relation.objects.get(userFollowed=pk, userFollowing=userid)
            return self.list(request, *args, **kwargs)
        except Relation.DoesNotExist:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        userid = self.request.user.id
        boardid = self.kwargs.get('boardid')
        board = Board.objects.get(id=boardid)
        pk = board.user.id
        if pk != userid:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateBoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "Added"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        userid = self.request.user.id
        boardid = self.kwargs.get('boardid')
        board = Board.objects.get(id=boardid)
        pk = board.user.id
        if pk != userid:
            return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        board.delete()
        return JsonResponse({"status": "Deleted"}, status=status.HTTP_200_OK)


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
