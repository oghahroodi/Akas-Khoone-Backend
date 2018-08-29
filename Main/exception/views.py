from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # print(response.data['detail'])
        response.data['status'] = response.data['detail']
        response.data['status_code'] = response.status_code
        # print(response.data)
    return response