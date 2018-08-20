from rest_framework.views import APIView

class sendPosts(APIView):
    def get(self, request):
        userid = request.user.id