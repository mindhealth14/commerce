# Generated by Django 4.2.5 on 2023-10-03 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_rename_image_url_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, default=None, max_length=228, null=True),
        ),
    ]
