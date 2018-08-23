from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import User,Person,Post



factory = APIRequestFactory()
client = APIClient()


class ModelTestCase(TestCase):

    
    def setUp(self):
        self.User.objects.create(username='test1',password='test1pass')
        self.User.objects.create(username='test2',password='test2pass')
        self.User.objects.create(username='test3',password='test3pass')
        self.User.objects.create(username='test4',password='test4pass')
        self.User.objects.create(username='test5',password='test5pass')
        self.User.objects.create(username='test6',password='test6pass')
        self.User.objects.create(username='test7',password='test7pass')
        self.User.objects.create(username='test8',password='test8pass')
        self.User.save()

    def testPostModel(self):
        self.assert("fef")
        self.a = User.objects.get(name='test1')
        self.assertEqual(a.__repr__(), "Casper belongs to Bull Dog breed.")

