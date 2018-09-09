"""Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Notifications.producers import connect

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('Core.urls')),
    path('', include('Account.urls')),
    path('', include('Post.urls')),
    path('', include('Search.urls')),

    path('', include('Social.urls')),
    path('', include('Notification.urls'))

]

connect()
# key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
# print ('key', [x for x in key])
# iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
# aes = AES.new(key, AES.MODE_CBC, iv)
# data = 'hello world 1234' # <- 16 bytes
# encd = aes.encrypt(data)
# aes = AES.new(key, AES.MODE_CBC, iv)
# decd = adec.decrypt(encd)
# print (decd)
