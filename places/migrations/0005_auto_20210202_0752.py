# Generated by Django 3.1.5 on 2021-02-02 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_auto_20210202_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='properties_placeId',
            field=models.CharField(default='', max_length=200, verbose_name='Уникальный идентификатор локации'),
        ),
        migrations.AlterField(
            model_name='location',
            name='properties_title',
            field=models.CharField(default='', max_length=200, verbose_name='Название для точки'),
        ),
        migrations.AlterField(
            model_name='location',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название для боковой панели'),
        ),
    ]
