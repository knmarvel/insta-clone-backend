from django.db import models
from authentication.models import Author
from insta_backend.models import Post

class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )
    creator = models.ForeignKey(Author, related_name='creator', on_delete=models.CASCADE)
    to = models.ForeignKey(Author, related_name='to', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, default='None', on_delete=models.CASCADE)
    

    def __str__(self):
        return '{} - {}'.format(self.notification_type, self.post)