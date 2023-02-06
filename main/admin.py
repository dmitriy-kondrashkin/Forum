from django.contrib import admin
from.models import Post, Vote, Comment, CommentReply
# Register your models here.
admin.site.register(Vote)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentReply)