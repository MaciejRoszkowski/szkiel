# Generated by Django 2.0.2 on 2018-06-16 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20180616_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
