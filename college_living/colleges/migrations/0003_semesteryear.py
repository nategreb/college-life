# Generated by Django 4.0.4 on 2022-12-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('colleges', '0002_collegeclasses_department_professor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemesterYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=11)),
            ],
        ),
    ]
