# Generated by Django 4.0.4 on 2022-12-03 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('colleges', '0002_collegeclasses_department_professor_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('term_year', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=160)),
                ('test_heavy', models.PositiveSmallIntegerField()),
                ('usefulness', models.PositiveSmallIntegerField()),
                ('theoretical', models.PositiveSmallIntegerField()),
                ('take_again', models.PositiveSmallIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='colleges.collegeclasses')),
                ('term', models.ManyToManyField(to='college_reviews.term')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='coursereview',
            constraint=models.CheckConstraint(check=models.Q(('take_again__isnull', False), ('take_again__range', (1, 5)), ('test_heavy__isnull', False), ('test_heavy__range', (1, 5)), ('theoretical__isnull', False), ('theoretical__range', (1, 5)), ('usefulness__isnull', False), ('usefulness__range', (1, 5))), name='check_review'),
        ),
        migrations.AddConstraint(
            model_name='coursereview',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='user_course'),
        ),
    ]