# Generated by Django 5.1.1 on 2024-09-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='value',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
