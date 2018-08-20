from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from Core.personModels import Person
from Core.personSerializer import PersonSerializer
from django.http import JsonResponse

class sendInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.filter(user=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer)