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
