from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Core.models import Person
from Core.serializers import PersonSerializer, UserSerializer
from django.http import JsonResponse

class SendInfo(APIView):
    def get(self, request):
        userid = request.user.id
        person = Person.objects.get(user__id=userid)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)

class CreateUser(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return JsonResponse({'status': 'CREATED'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckUsername(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse({'status': 'ACCEPTED'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)