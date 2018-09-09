from Account.models import Relation
from rest_framework import status
from django.http import JsonResponse


#def extractHashtags(s):
    #return re.findall(r"#(\w+)", s)
    #return set(part[1:] for part in s.split() if part.startswith('#'))


def authorizeUser(pk, userid):
    try:
        print(pk, userid)
        if pk != userid:
            Relation.objects.get(userFollowed=pk, userFollowing=userid)
    except Relation.DoesNotExist:
        print("return")
        return JsonResponse({"status": "Not_Authorized"}, status=status.HTTP_401_UNAUTHORIZED)