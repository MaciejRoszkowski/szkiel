# Generated by Django 2.0.2 on 2018-06-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='passwd',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]