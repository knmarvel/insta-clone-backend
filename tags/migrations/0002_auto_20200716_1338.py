# Generated by Django 3.0.8 on 2020-07-16 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta_backend', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('post', models.ManyToManyField(blank=True, related_name='tagged_posts', to='insta_backend.Post')),
            ],
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]