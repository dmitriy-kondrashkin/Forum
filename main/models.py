from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    slug = models.SlugField('Post slug', null=False, blank=False, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('main:post-detail', kwargs=kwargs)

    def __str__(self):
        return f'{self.title}'
    
    @property
    def get_comment_numbers(self):
        return Comment.objects.filter(post=self).count()

    
class Vote(models.Model):
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})    
        
    def __str__(self):
        return f'Comment by "{self.author}" to post "{self.post}"'


class CommentReply(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(timezone.now())
    
    class Meta:
        ordering = ['created_at']    

    def __str__(self):
        return f'Reply by {self.author} to comment by {self.comment.author}'