from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from Core.models import Person
from Core.serializers import PostSerializer
from django.http import JsonResponse

class sendInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.filter(user=userid)
        serializer = PostSerializer(person)
        return JsonResponse(serializer)


    #salam
