# Generated by Django 4.2.5 on 2023-10-01 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_bid_win_list_winner_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.product'),
        ),
    ]