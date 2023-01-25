# Generated by Django 4.0.4 on 2023-01-25 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(blank=True, max_length=32, verbose_name='Identifier')),
                ('counts_for_average', models.BooleanField(default=True, verbose_name='Counts for average rating')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField(blank=True, max_length=1024, verbose_name='Content')),
                ('language', models.CharField(blank=True, max_length=5, verbose_name='Language')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('average_rating', models.FloatField(default=0, verbose_name='Average rating')),
                ('extra_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('extra_content_type',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='reviews_attached', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='ReviewExtraInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256, verbose_name='Type')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review',
                                             verbose_name='Review')),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='RatingCategoryChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=20, null=True, verbose_name='Value')),
                ('label', models.CharField(max_length=128, verbose_name='Label')),
                ('ratingcategory',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices',
                                   to='reviews.ratingcategory', verbose_name='Rating category')),
            ],
            options={
                'ordering': ('-value',),
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value',
                 models.CharField(blank=True, choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
                                  max_length=20, null=True, verbose_name='Value')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.ratingcategory',
                                               verbose_name='Category')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings',
                                             to='reviews.review', verbose_name='Review')),
            ],
            options={
                'ordering': ['category', 'review'],
            },
        ),
    ]
