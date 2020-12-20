from django.urls import include, path
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import UserProfile


# Create your tests here.


class EmployeeTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('employee.urls')),
    ]

    def setUp(self):
        self.user = UserProfile.objects.create(name='Uwe', email='uwe@gmail.com', password='kigali')
        self.response = self.client.get('http://127.0.0.1:5000/api/employee/')

    def test_display_all_employee(self):
        """ Ensure we get all employee."""

        response = self.client.get('http://127.0.0.1:5000/api/employee/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_employee(self):
        """ Ensure we post new employee."""

        data = {'name': 'Uwe', 'email': 'uweaime@gmail.com', 'password': 'kigali'}
        response = self.client.post('http://127.0.0.1:5000/api/employee/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)


