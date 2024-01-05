# Generated by Django 4.2.5 on 2023-12-10 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_product_current_bid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product']},
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id'], name='auctions_pr_id_e7c6fb_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product'], name='auctions_pr_product_dd3c53_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['listed_date'], name='auctions_pr_listed__81a1ee_idx'),
        ),
    ]