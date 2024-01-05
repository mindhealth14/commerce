# Generated by Django 4.2.5 on 2023-10-03 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_winner_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(blank=True, default=None, max_length=228, null=True),
        ),
    ]
