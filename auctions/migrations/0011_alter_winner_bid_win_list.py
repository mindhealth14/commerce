# Generated by Django 4.2.5 on 2023-10-01 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_comment_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='bid_win_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auctions.product'),
        ),
    ]
