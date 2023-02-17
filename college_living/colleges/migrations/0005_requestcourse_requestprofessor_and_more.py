# Generated by Django 4.0.4 on 2023-02-17 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('colleges', '0004_alter_collegecourse_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=15, verbose_name='unique ID of the course')),
                ('course_name', models.CharField(max_length=90, verbose_name='name of course')),
            ],
        ),
        migrations.CreateModel(
            name='RequestProfessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='professor',
            name='courses',
            field=models.ManyToManyField(blank=True, to='colleges.collegecourse'),
        ),
        migrations.AddConstraint(
            model_name='collegecourse',
            constraint=models.UniqueConstraint(fields=('course_id',), name='secondary_course_id_key'),
        ),
        migrations.AddField(
            model_name='requestprofessor',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college'),
        ),
        migrations.AddField(
            model_name='requestprofessor',
            name='courses',
            field=models.ManyToManyField(to='colleges.collegecourse'),
        ),
        migrations.AddField(
            model_name='requestprofessor',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='colleges.department'),
        ),
        migrations.AddField(
            model_name='requestcourse',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college'),
        ),
        migrations.AddField(
            model_name='requestcourse',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='colleges.department'),
        ),
        migrations.AddConstraint(
            model_name='requestprofessor',
            constraint=models.UniqueConstraint(fields=('college', 'department', 'first_name', 'last_name'),
                                               name='request_prof_alt_key'),
        ),
        migrations.AddConstraint(
            model_name='requestcourse',
            constraint=models.UniqueConstraint(fields=('college', 'department', 'course_name', 'course_id'),
                                               name='req_course_alt_key'),
        ),
        migrations.AddConstraint(
            model_name='requestcourse',
            constraint=models.UniqueConstraint(fields=('course_id',), name='secondary_course_id_key_request_course'),
        ),
    ]
