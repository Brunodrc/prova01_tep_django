# Generated by Django 4.1.7 on 2023-05-03 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_wallet', '0004_alter_stock_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_done',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
