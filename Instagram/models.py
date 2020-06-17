from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class InstagramUser(AbstractUser):
    profile_picture = ProcessedImageField(
        upload_to = 'static/images/profile_images',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(follower=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(followee=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(followee=self)
        return followers.filter(followor=user).exists()

    def get_absolute_url(self):
        return reverse('user', args=[str(self.id)])

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name="following_set")
    followee = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name="followed_by_set")

    class Meta:
        unique_together = ("follower", "followee")

    def __str__(self):
        return self.follower.username + ' follows ' + self.followee.username

class Post(models.Model):
    author = models.ForeignKey(
        InstagramUser,
        on_delete = models.CASCADE,
        related_name = 'posts'
    )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'likes'
    )
    user = models.ForeignKey(
        InstagramUser,
        on_delete = models.CASCADE,
        related_name = 'likes'
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return self.user.username + " likes " + self.post.author.username + "'s post with ID: " + str(self.post.pk)

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'comments'
    )
    user = models.ForeignKey(
        InstagramUser,
        on_delete = models.CASCADE,
        related_name = 'comments'
    )
    comment = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.user.username + " commented " + self.post.author.username + "'s post with ID: " + str(self.post.pk)