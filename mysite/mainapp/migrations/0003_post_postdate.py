# Generated by Django 2.0.2 on 2018-06-15 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20180611_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
