import re



def contactState(index):
    if index == 0:
        return "friend"
    if index == 1:
        return "registered"
    if index == 2:
        return "notregistered"

def makeRelation(following,followed):
    return {'userFollowing': following, 'userFollowed':followed}

def makeMail(code):
    return "کد ورودی برای فراموشی رمز عبور:\n" + code


