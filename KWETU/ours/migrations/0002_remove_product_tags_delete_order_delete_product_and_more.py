# Generated by Django 4.0 on 2021-12-24 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ours', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
