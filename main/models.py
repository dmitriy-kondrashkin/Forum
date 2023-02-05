from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk})   

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