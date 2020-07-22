import re
from tags.models import Tag
from authentication.models import Author
from insta_backend.models import Post
from notification.models import Notification


def notify_helper(creator, post, type):
    notify = Notification.objects.create(
            creator=creator,
            to=post.author,
            notification_type=type,
            post=post,
            seen=False
        )
    return notify


def notify_follow_helper(creator, to, type):
    notify = Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=type,
        seen=False
    )
    return notify


def check_for_tags(text, post_id, creator):
    """Checks text string for captions and returns html for words"""
    if "#" or "@" in text:
        tag_re = r'\B#\w*[a-zA-Z]+\w*'
        for tag in set(re.findall(tag_re, text)):
            selected_tag = Tag.objects.get_or_create(text=tag[1:])[0]
            tagged_post = Post.objects.get(id=post_id)
            selected_tag.post.add(tagged_post)
            selected_tag.save()
            new_tag = f"<a href='/tag/{tag[1:]}'>{tag}</a>"
            text = text.replace(tag, new_tag)
        user_re = r'\B@\w*[a-zA-Z]+\w*'
        for username in set(re.findall(user_re, text)):
            user = Author.objects.get(username=username[1:])
            if user:
                post = Post.objects.get(id=post_id)
                notify_helper(creator, post, 'mention')
                new_username = f"<a href='/user/{username[1:]}'>{username}</a>"
                text = text.replace(username, new_username)
    return text


