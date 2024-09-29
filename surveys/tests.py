from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestMyModelSetup(TestCase):
    def setUp(self):
        self.client = APIClient()


class TestMySurveysAPIs(TestMyModelSetup):
    def test_get_all_surveys(self):
        response = self.client.get('/surveys/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_add_survey(self):
        data = {"title": "survey 1", "description": "some description..."}
        response = self.client.post('/surveys/?question_ids=1&question_ids=2', data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)