# Generated by Django 3.0.8 on 2020-07-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200723_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='yayin_taslak',
            field=models.CharField(choices=[('yayin', 'YAYIN'), ('taslak', 'TASLAK')], default='yayin', max_length=6),
        ),
    ]