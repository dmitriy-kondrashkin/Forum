from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string

# Create your models here.
class Post(models.Model):
    slug = models.SlugField('Post slug', max_length=150, null=False, blank=False, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField(get_user_model(), related_name='votes', blank=True)

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('main:post-detail', kwargs=kwargs)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        if Post.objects.filter(title=self.title).exists():
            value = f'{get_random_string(length=2)}{self.title}{get_random_string(length=4)}'
            self.slug = slugify(value, allow_unicode=True)
        else:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    @property
    def get_comment_numbers(self):
        return Comment.objects.filter(post=self).count()
    
    @property
    def votes_count(self):
        return self.votes.count()


class Comment(models.Model):
    slug = models.SlugField('Comment slug', max_length=150, null=False, blank=False, unique=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    reply = models.ForeignKey('Comment' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if Comment.objects.filter(content=self.content).exists():
            value = f'{get_random_string(length=2)}{self.content}{get_random_string(length=4)}'
            self.slug = slugify(value, allow_unicode=True)
        else:
            self.slug = slugify(self.content, allow_unicode=True)
        super(Comment, self).save(*args, **kwargs)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    def num_of_replies(self):
        return Comment.objects.filter(reply=self).count()
        

    def get_absolute_url(self):
        kwargs = {'slug': self.post.slug}
        return reverse('main:post-detail', kwargs=kwargs)

    def __str__(self):
        return f'Comment by "{self.author}" to post "{self.post}"'
