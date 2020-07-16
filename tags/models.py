from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Tag(models.Model):
    text = models.TextField(max_length=500)
    post = models.ManyToManyField(
        'insta_backend.Post',
        blank=True,
        related_name="tagged_posts")
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return f"{self.text}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        return super().save(*args, **kwargs)
