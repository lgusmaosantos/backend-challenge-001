"""
Posts testing
"""
###
# Libraries
###
from django.contrib.auth import get_user_model
from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from topic.models import Topic
from .models import Post


User = get_user_model()

###
# Test Cases
###
class PostVisualizationTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        self.user2 = User.objects.create(
            username='user2',
            password=password_example
        )

        # Creating a few topics by both users
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

        # Creating a few posts in both topics
        self.post1 = Post.objects.create(
            author=self.user1,
            title='Post 1',
            content='Rich content 1',
            topic=self.topic1
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            title='Post 2',
            content='Rich content 2',
            topic=self.topic1
        )
        self.post3 = Post.objects.create(
            author=self.user1,
            title='Post 3',
            content='Rich content 3',
            topic=self.topic2
        )
    
    def test_list_posts_on_topic(self):
        """Tests the exhibition of the posts concerning
        a topic.
        """
        url = reverse('post-list', args=[self.topic1.url_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_post_on_topic(self):
        """Tests the exhibion of a specific post concerning
        a topic.
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], self.post1.id)
        self.assertEqual(data['title'], self.post1.title)


class PostCreationTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)

        # Creating a few topics by both users
        self.topic1 = Topic.objects.create(
            title='Title 1',
            author=self.user1,
            description='Description',
            url_name='title1'
        )

    def test_post_creation_success(self):
        """The success case for the creation of a post."""
        url = reverse('post-list', args=[self.topic1.url_name])
        payload = {
            'author': self.user1.id,
            'title': 'Creating a post',
            'content': 'Rich content 4',
        }
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.user1.auth_token.key
        )
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_post = Post.objects.filter(
            author=self.user1,
            title=payload.get('title'),
            content=payload.get('content'),
            topic=self.topic1
        )
        self.assertTrue(new_post.exists())

    def test_post_creation_unauthenticated(self):
        """Tests if it's possible for an unauthenticated user
        to create a post (it shouldn't be).
        """
        url = reverse('post-list', args=[self.topic1.url_name])
        payload = {
            'author': self.user1.id,
            'title': 'Creating a post while being unauthenticated',
            'content': 'Rich content 5',
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        new_post = Post.objects.filter(
            author=self.user1,
            title=payload.get('title'),
            content=payload.get('content'),
            topic=self.topic1
        )
        self.assertFalse(new_post.exists())


class PostUpdateTestCase(APITestCase):
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

        self.post1 = Post.objects.create(
            author=self.user1,
            title='Post 1',
            content='Rich content 1',
            topic=self.topic1
        )

    def test_post_update_sucess(self):
        """The success case for a post update."""
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        payload = {
            'title': 'Updated title',
            'content': 'Updated content'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.user1.auth_token.key
        )
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = Post.objects.filter(
            id=self.post1.id,
            author=self.user1,
            title=payload.get('title'),
            content=payload.get('content')
        )
        self.assertTrue(updated_post.exists())


    def test_post_update_unauthenticated(self):
        """Tests if an unauthenticated user could perform
        a post update (they shouldn't).
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        payload = {
            'title': 'Updated title',
            'content': 'Updated content'
        }
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        updated_post = Post.objects.filter(
            id=self.post1.id,
            author=self.user1,
            title=payload.get('title'),
            content=payload.get('content')
        )
        self.assertFalse(updated_post.exists())

    def test_update_post_by_another_user(self):
        """Tests if it's possible for a user to update another
        user's post.
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        payload = {
            'title': 'Updated title',
            'content': 'Updated content'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.user2.auth_token.key
        )
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_post = Post.objects.filter(
            id=self.post1.id,
            author=self.user1,
            title=payload.get('title'),
            content=payload.get('content')
        )
        self.assertFalse(updated_post.exists())


class PostDeletionTestCase(APITestCase):
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

        self.post1 = Post.objects.create(
            author=self.user1,
            title='Post 1',
            content='Rich content 1',
            topic=self.topic1
        )

    def test_post_deletion_success(self):
        """The success case for the deletion of
        a post.
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.user1.auth_token.key
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_post = Post.objects.filter(
            id=self.post1.id,
        )
        self.assertFalse(updated_post.exists())

    def test_post_deletion_unauthenticated(self):
        """Tests if an unauthenticated user is able to
        delete a post (they shouldn't be).
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        updated_post = Post.objects.filter(
            id=self.post1.id,
        )
        self.assertTrue(updated_post.exists())

    def test_delete_post_by_another_user(self):
        """Tests if it's possible for a user to delete a post
        not created by them.
        """
        url = reverse(
            'post-detail',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.user2.auth_token.key
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_post = Post.objects.filter(
            id=self.post1.id,
        )
        self.assertTrue(updated_post.exists())
