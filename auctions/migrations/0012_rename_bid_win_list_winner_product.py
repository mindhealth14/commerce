# Generated by Django 4.2.5 on 2023-10-01 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_winner_bid_win_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='winner',
            old_name='bid_win_list',
            new_name='product',
        ),
    ]