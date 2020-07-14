from django.db import models


class Comments(models.Model):
	comment_post = models.CharField(max_length=150)
	author = models.ForeignKey('authentication.Author', related_name='commenter', on_delete=models.CASCADE)
	commented_image = models.ForeignKey('insta_backend.Post', on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username
