import uuid
from time import time

from django.contrib.auth import get_user_model
from django.db import models

from pytils.translit import slugify


User = get_user_model()

def gen_slug(s):
    slug = slugify(s)
    return slug + '-' + str(int(time()))


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True, blank=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    uuid = models.UUIDField(primary_key=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('price', )


class PostImage(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)


class Comment(models.Model):
    product = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField(max_length=400)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commment by {self.author} on {self.product}, created at {self.created_at}'
