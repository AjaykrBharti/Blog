# Generated by Django 2.1.15 on 2020-07-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogg', '0007_auto_20200728_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default=False, upload_to=''),
        ),
    ]
