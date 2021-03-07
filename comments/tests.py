"""
Comments testing
"""
###
# Libraries
###
from datetime import time
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from topic.models import Topic
from posts.models import Post
from .models import Comment


User = get_user_model()

###
# Test Cases
###
class CommentVisualizationTestCase(APITestCase):
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
        self.post2 = Post.objects.create(
            author=self.user2,
            title='Post 2',
            content='Rich content 2',
            topic=self.topic1
        )

        self.comment1 = Comment.objects.create(
            title='Title 1',
            author=self.user1,
            content='A smart addendum 1',
            post=self.post1
        )

        self.comment2 = Comment.objects.create(
            title='Title 2',
            author=self.user1,
            content='A smart addendum 2',
            post=self.post1
        )

        self.comment3 = Comment.objects.create(
            title='Title 3',
            author=self.user2,
            content='A smart addendum 3',
            post=self.post2
        )

    def test_list_comments_on_post(self):
        url = reverse(
            'comment-list',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_comment_on_post(self):
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment2.id
            ]
        )
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], self.comment2.id)
        self.assertEqual(data['title'], self.comment2.title)
        self.assertEqual(data['content'], self.comment2.content)


class CommentCreationTestCase(APITestCase):
    def setUp(self):
        password_example = 'userrules'
        self.user1 = User.objects.create(
            username='user1',
            password=password_example
        )
        Token.objects.create(user=self.user1)

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

    def test_comment_creation_success(self):
        """The success case for the creation of a comment."""
        url = reverse(
            'comment-list',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        payload = {
            'title': 'Title 4',
            'content': 'A smart addendum 4',
            'post': self.post1
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_comment = Comment.objects.filter(
            author=self.user1,
            post=self.post1,
            title=payload.get('title'),
            content=payload.get('content')
        )
        self.assertTrue(new_comment.exists())

    def test_comment_creation_unauthenticated(self):
        """Tests if an unauthenticated user is able to
        create a comment (they shouldn't be).
        """
        url = reverse(
            'comment-list',
            args=[
                self.topic1.url_name,
                self.post1.id
            ]
        )
        payload = {
            'title': 'Title 5',
            'content': 'A smart addendum 5',
            'post': self.post1
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        new_comment = Comment.objects.filter(
            author=self.user1,
            post=self.post1,
            title=payload.get('title'),
            content=payload.get('content')
        )
        self.assertFalse(new_comment.exists())


class CommentUpdateTestCase(APITestCase):
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

        self.comment1 = Comment.objects.create(
            title='Title 1',
            author=self.user1,
            content='A smart addendum 1',
            post=self.post1
        )

    def test_comment_update_success(self):
        """The success case for the update of a comment."""
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        payload = {
            'content': 'An interesting counter-argument.'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = Comment.objects.filter(
            post=self.post1,
            author=self.user1,
            content=payload.get('content')
        )
        self.assertTrue(updated_comment.exists())

    def test_comment_update_unauthenticated(self):
        """Tests if it's possible for an unauthenticated
        user to update a comment (it shouldn't be)."""
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        payload = {
            'content': 'An interesting counter-argument.'
        }
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        updated_comment = Comment.objects.filter(
            post=self.post1,
            author=self.user1,
            content=payload.get('content')
        )
        self.assertFalse(updated_comment.exists())

    def test_comment_update_by_another_user(self):
        """Tests if it's possible for an user to update a comment
        made by someone else (it shouldn't be).
        """
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        payload = {
            'content': 'An interesting counter-argument.'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key
        )
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_comment = Comment.objects.filter(
            post=self.post1,
            author=self.user1,
            content=payload.get('content')
        )
        self.assertFalse(updated_comment.exists())


class CommentDeletionTestCase(APITestCase):
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

        self.comment1 = Comment.objects.create(
            title='Title 1',
            author=self.user1,
            content='A smart addendum 1',
            post=self.post1
        )        

    def test_comment_deletion_success(self):
        """The success case for the deletion of a comment."""
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deleted_comment = Comment.objects.filter(
            id=self.comment1.id
        )
        self.assertFalse(deleted_comment.exists())

    def test_comment_deletion_unauthenticated(self):
        """Tests if it's possible for an unauthenticated user to
        delete a comment (it shouldn't be).
        """
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        deleted_comment = Comment.objects.filter(
            id=self.comment1.id
        )
        self.assertTrue(deleted_comment.exists())

    def test_comment_deletion_by_another_user(self):
        """Tests if it's possible for an user to delete a comment
        they didn't create (it shouldn't be).
        """
        url = reverse(
            'comment-detail',
            args=[
                self.topic1.url_name,
                self.post1.id,
                self.comment1.id
            ]
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        deleted_comment = Comment.objects.filter(
            id=self.comment1.id
        )
        self.assertTrue(deleted_comment.exists())
