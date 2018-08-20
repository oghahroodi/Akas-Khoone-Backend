import json
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework_jwt.settings import api_settings


# @api_view(['GET'])
# def login(request):
#
#     print("got a request")
#     if request.method == 'POST':
#         json_data = json.loads(request.body)
#         username = json_data['username']
#         password = json_data['password']
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#
#             jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#             jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#
#             user_details = {}
#             user_details['username'] = user.username
#             user_details['token'] = token
#             return JsonResponse(user_details, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({'err': '1', 'errlog': 'username or pass is wrong'})


