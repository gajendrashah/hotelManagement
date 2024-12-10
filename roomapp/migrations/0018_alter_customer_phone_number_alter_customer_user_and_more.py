# Generated by Django 4.0.5 on 2022-09-26 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0017_alter_booked_number_of_days_alter_customer_main_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(help_text='Contact phone number', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(default='#WYMJ62', max_length=255),
        ),
        migrations.AlterField(
            model_name='non_room_user',
            name='order_id',
            field=models.CharField(default='#W6PEES', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='#C1DHIU', max_length=255, unique=True),
        ),
    ]