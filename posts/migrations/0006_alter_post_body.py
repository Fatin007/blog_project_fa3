# Generated by Django 5.1.7 on 2025-04-07 13:55

from django.db import migrations
from django_ckeditor_5.fields import CKEditor5Field


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=CKEditor5Field(config_name='extends'),
        ),
    ]
