# Generated by Django 2.0.4 on 2018-05-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20180426_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='auther',
            field=models.CharField(default='佚名', max_length=100),
        ),
    ]