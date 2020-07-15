from django.db import models
from django.utils import timezone

from insta_backend.models import Post


class Comments(models.Model):
	posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
	                          blank=True, related_name='comment_text')
	author = models.ForeignKey('authentication.Author', max_length=200, on_delete=models.CASCADE)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text
