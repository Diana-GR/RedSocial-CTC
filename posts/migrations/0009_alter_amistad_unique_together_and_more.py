# Generated by Django 5.1 on 2024-09-17 05:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_post_reacciones_remove_post_likes_post_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='amistad',
            unique_together={('usuario', 'amigo')},
        ),
        migrations.AddConstraint(
            model_name='amistad',
            constraint=models.UniqueConstraint(fields=('usuario', 'amigo'), name='unique_friendship'),
        ),
    ]
