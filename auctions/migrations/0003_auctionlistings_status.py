# Generated by Django 4.1.3 on 2022-12-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
