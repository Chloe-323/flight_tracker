# Generated by Django 4.1.3 on 2022-12-05 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='purchase_time',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='purchase_date',
            field=models.DateTimeField(),
        ),
    ]