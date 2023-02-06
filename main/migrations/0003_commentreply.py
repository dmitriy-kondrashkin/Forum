# Generated by Django 4.1.4 on 2023-02-06 04:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 6, 4, 56, 23, 466708, tzinfo=datetime.timezone.utc))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.comment')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
