# Generated by Django 5.0.4 on 2024-04-28 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kobanchik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='liked_bars', to='kobanchik.customuser'),
        ),
    ]
