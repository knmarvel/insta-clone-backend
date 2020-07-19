from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class AuthorManager(BaseUserManager):
    def create_user(self, email, name, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not username:
            raise ValueError('Users must have a username')
        author = self.model(
            email=self.normalize_email(email),
            name = name,
            username = username
        )
        author.set_password(password)
        author.save(using=self._db)
        return author
    
    def create_staffuser(self, email, name, username, password):
        author = self.create_user(
            email,
            name,
            username,
            password=password
        )
        author.staff = True
        author.save(using=self._db)
        return author

    def create_superuser(self, email, name, username, password):
        author = self.create_user(
            email,
            name,
            username,
            password=password
        )
        author.staff = True
        author.admin = True
        author.save(using=self._db)
        return author


class Author(AbstractBaseUser):
    
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=False, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    
    following = models.ManyToManyField(
        'self',
        related_name="following"
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    objects = AuthorManager()

class Profile(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=280, blank=True)
    website = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(null=True, blank=True, default='default.png', upload_to='profile_uploads')
    location = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.user.name
    

@receiver(post_save, sender=Author)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

@receiver(post_save, sender=Author)
def save_author_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()
    