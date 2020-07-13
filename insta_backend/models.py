from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        'authentication.Author',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='post_uploads/')
    caption = models.TextField(max_length=500)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        'authentication.Author',
        blank=True,
        related_name="authors_who_like_this"
        )

    def __str__(self):
        return f"{self.author.name} Pic {self.id}"
    