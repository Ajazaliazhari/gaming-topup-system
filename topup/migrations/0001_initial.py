# Generated by Django 5.1.5 on 2025-06-16 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="The common name of the game (e.g., 'PUBG Mobile').", max_length=255, unique=True)),
                ('game_id', models.CharField(help_text="A unique identifier for the game (e.g., 'pubg123').", max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True, help_text='Indicates if the game is currently active for top-ups.')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TopUpProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Name of the top-up product (e.g., 'UC Pack 500').", max_length=255)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of the top-up product in local currency.', max_digits=10)),
                ('in_game_currency', models.CharField(help_text="Amount or type of in-game currency (e.g., '500 UC', '1000 Diamonds').", max_length=100)),
                ('game', models.ForeignKey(help_text='The game this top-up product belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='topup.game')),
            ],
            options={
                'verbose_name': 'Top-Up Product',
                'verbose_name_plural': 'Top-Up Products',
                'ordering': ['game__name', 'name'],
                'unique_together': {('game', 'name')},
            },
        ),
        migrations.CreateModel(
            name='TopUpOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(help_text='Email of the user who made the top-up order.', max_length=254)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', help_text='Current status of the top-up order.', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the order was created.')),
                ('product', models.ForeignKey(help_text='The top-up product purchased.', on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='topup.topupproduct')),
            ],
            options={
                'verbose_name': 'Top-Up Order',
                'verbose_name_plural': 'Top-Up Orders',
                'ordering': ['-created_at'],
            },
        ),
    ]
