"""
Topic testing
"""
###
# Libraries
###
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Topic


User = get_user_model()

###
# Test Cases
###
class TopicVisualizationTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)
        self.user2 = User.objects.create(
            username='user2',
            password=password_example
        )
        Token.objects.create(user=self.user2)

        # Creating a few topics by both users
        # (2 by user1, 1 by user2)
        self.topic1 = Topic.objects.create(
            title='Title 1',
            author=self.user1,
            description='Description',
            url_name='title1'
        )
        self.topic2 = Topic.objects.create(
            title='Title 2',
            author=self.user1,
            description='Description',
            url_name='title2'
        )
        self.topic3 = Topic.objects.create(
            title='Title 3',
            author=self.user2,
            description='Description',
            url_name='title3'
        )
    
    def test_list_topics_success(self):
        """Tests the listing of all topics regardless of author.
        For this view, all topics should be displayed."""
        url = reverse('topic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_get_specific_topic_success(self):
        """Tests the exhibition of a topic's details """
        url = reverse('topic-detail', args=[self.topic1.url_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.topic1.title)
        self.assertEqual(response.data['url_name'], self.topic1.url_name)


class TopicCreationTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)
    
    def test_create_topic_success(self):
        """The success case for the creation of a topic."""
        url = reverse('topic-list')
        payload = {
            'title': 'Django Tips',
            'author': self.user1.id,
            'description': 'Top tips from professional Django developers',
            'url_name': 'django-tips'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        topic_with_url_name = Topic.objects.filter(
            url_name=payload.get('url_name')
        )
        self.assertTrue(topic_with_url_name.exists())

    def test_create_topic_unauthenticated(self):
        """Tests the creation of a topic by an unauthenticated
        user (`AnonymousUser`). Such users shouldn't be able
        to create topics.
        """
        url = reverse('topic-list')
        payload = {
            'title': 'Python Tips',
            'author': self.user1.id,
            'description': 'Top tips from professional Python developers',
            'url_name': 'python-tips'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        topic_with_url_name = Topic.objects.filter(
            url_name=payload.get('url_name')
        )
        self.assertFalse(topic_with_url_name.exists())


class TopicUpdateTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)
        self.user2 = User.objects.create(
            username='user2',
            password=password_example
        )
        Token.objects.create(user=self.user2)

        # Creating a few topics by both users
        self.topic1 = Topic.objects.create(
            title='Title 1',
            author=self.user1,
            description='Description',
            url_name='title1'
        )
        self.topic2 = Topic.objects.create(
            title='Title 2',
            author=self.user2,
            description='Description',
            url_name='title2'
        )

    def test_topic_update_success(self):
        """The sucess case for a topic update."""
        url = reverse('topic-detail', args=[self.topic1.url_name])
        payload = {
            'description': 'A slightly better description',
            'title': 'An alluring title'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['id'], self.topic1.id)
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['description'], payload['description'])

    def test_topic_update_unauthenticated(self):
        """Tests if an unauthenticated user could perform
        a topic update (they shouldn't).
        """
        url = reverse('topic-detail', args=[self.topic1.url_name])
        payload = {
            'description': 'A failing request description',
            'title': 'A failing request title'
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.topic1.refresh_from_db()
        self.assertNotEqual(payload['description'], self.topic1.description)
        self.assertNotEqual(payload['title'], self.topic1.title)

    def test_update_topic_by_another_user(self):
        """Tests if it's possible for an user to edit a topic
        created by another user (it shouldn't be).
        """
        url = reverse('topic-detail', args=[self.topic2.url_name])
        payload = {
            'description': 'A failing request description',
            'title': 'A failing request title'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.topic2.refresh_from_db()
        self.assertNotEqual(payload['description'], self.topic2.description)
        self.assertNotEqual(payload['title'], self.topic2.title)


class TopicDeletionTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)
        self.user2 = User.objects.create(
            username='user2',
            password=password_example
        )
        Token.objects.create(user=self.user2)

        self.topic1 = Topic.objects.create(
            title='Title 1',
            author=self.user1,
            description='Description',
            url_name='title1'
        )
    
    def test_topic_deletion_success(self):
        """The success case for a topic's deletion."""
        url = reverse('topic-detail', args=[self.topic1.url_name])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        topic_qs = Topic.objects.filter(id=self.topic1.id)
        self.assertFalse(topic_qs.exists())

    def test_topic_deletion_unauthenticated(self):
        """Tests if it's possible for an unauthenticated user
        to delete a topic record (it shouldn't be).
        """
        url = reverse('topic-detail', args=[self.topic1.url_name])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        topic_qs = Topic.objects.filter(id=self.topic1.id)
        self.assertTrue(topic_qs.exists())

    def test_topic_deletion_by_another_user(self):
        """Tests if it's possible for an user to delete a topic
        created by another user.
        """
        url = reverse('topic-detail', args=[self.topic1.url_name])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key
        )
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        topic_qs = Topic.objects.filter(id=self.topic1.id)
        self.assertTrue(topic_qs.exists())
