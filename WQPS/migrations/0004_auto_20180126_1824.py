# Generated by Django 2.0.1 on 2018-01-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WQPS', '0003_remove_waterqualityrecord_codmn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='waterqualityrecord',
            options={'ordering': ['station', 'year', 'month']},
        ),
        migrations.AddField(
            model_name='waterqualityrecord',
            name='station',
            field=models.IntegerField(default=0, verbose_name='监测站编号'),
        ),
    ]
