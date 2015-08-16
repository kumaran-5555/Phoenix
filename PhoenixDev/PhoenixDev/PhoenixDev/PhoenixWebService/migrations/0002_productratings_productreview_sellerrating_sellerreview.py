# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhoenixWebService', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRatings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('productId', models.IntegerField(unique=True)),
                ('userId', models.IntegerField(unique=True)),
                ('ratingVal', models.IntegerField()),
                ('ratingTimestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('productId', models.IntegerField(unique=True)),
                ('userId', models.IntegerField(unique=True)),
                ('reviewVal', models.CharField(max_length=1024)),
                ('ratingTimestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SellerRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sellerId', models.IntegerField(unique=True)),
                ('userId', models.IntegerField(unique=True)),
                ('ratingVal', models.IntegerField()),
                ('ratingTimestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SellerReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sellerId', models.IntegerField(unique=True)),
                ('userId', models.IntegerField(unique=True)),
                ('reviewVal', models.CharField(max_length=1024)),
                ('ratingTimestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
