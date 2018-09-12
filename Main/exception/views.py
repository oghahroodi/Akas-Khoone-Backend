from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # print(response.data['detail'])
        try:
            response.data['status'] = response.data['detail']
            response.data['status_code'] = response.status_code
        except KeyError:
            response.data['status'] = {"ایمیل یا رمز عبور اشتباه است."}
            return response
            
        
        # print(response.data)
    return response