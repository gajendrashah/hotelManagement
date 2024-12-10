# Generated by Django 4.0.5 on 2022-09-26 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0016_alter_booked_child_alter_booked_female_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked',
            name='number_of_days',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='main_id',
            field=models.ImageField(blank=True, null=True, upload_to='customer/id'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(default='#3GCRXM', max_length=255),
        ),
        migrations.AlterField(
            model_name='non_room_user',
            name='order_id',
            field=models.CharField(default='#OACE4C', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='#SUNRZK', max_length=255, unique=True),
        ),
    ]