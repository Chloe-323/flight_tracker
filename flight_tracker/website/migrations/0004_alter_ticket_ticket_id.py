# Generated by Django 4.0.6 on 2022-12-04 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_flight_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]