# Generated by Django 4.0.4 on 2023-02-14 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('colleges', '0003_remove_collegecourse_college_classes_alt_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegecourse',
            name='slug',
            field=models.SlugField(blank=True, max_length=90),
        ),
    ]
