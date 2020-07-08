import datetime as datetime
from django.db import models
from django.utils import timezone
from datetime import datetime
# Comment model:
#     -text
#     -author(foreign key)
#     -post (foreign key)
#     -datetime


class Comments(models.Model):
	text = models.TextField(max_length=250, blank=True, null=True)
	author = models.ForeignKey('authentication.Author', on_delete=models.CASCADE)
	post = models.ForeignKey('insta_backend.Post', on_delete=models.CASCADE)
	datetime = datetime.now ()
	timezone = timezone.now()
	likes = models.ManyToManyField('insta_backend.Post',related_name='authors_who_like_this')
