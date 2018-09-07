from django.http import JsonResponse
from rest_framework.views import APIView

from .models import *
# from .serializers import *


class SearchTags(APIView):
    def post(self, request):
        pass
