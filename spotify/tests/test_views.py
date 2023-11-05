from django.test import TestCase

from django.contrib.auth.models import User
from spotify.models import Post


class ViewTest(TestCase):
    fixtures = ['user.json', 'post.json']

    def test_single_post(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)
        expected_result = {
            'id': 1,
            'title': 'This is a test',
            'content': 'Lorem ipsum...',
            'author': {
                'id': 3,
                'username': 'ali.alavi',
            },
        }
        self.assertEqual(response.json(), expected_result)
