# Generated by Django 4.0.4 on 2022-08-17 15:40

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('email_domain', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('college_name', models.CharField(help_text='Please capitalize the name', max_length=100)),
                ('state_province', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=2)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='')),
                ('date_modified', models.DateField(auto_now=True, verbose_name='')),
                ('slug', models.SlugField(blank=True, max_length=110)),
                ('is_approved', models.BooleanField(blank=True, default=False)),
            ],
            managers=[
                ('all_colleges', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ResidentialArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_hall_name', models.CharField(help_text='Please capitalize the names', max_length=100, verbose_name='Residential Area Name')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='')),
                ('slug', models.SlugField(blank=True, max_length=110)),
                ('college', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
            ],
        ),
        migrations.CreateModel(
            name='Dorms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dorm_name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='')),
                ('slug', models.SlugField(blank=True, max_length=110)),
                ('college', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
                ('residentialArea', models.ForeignKey(blank=True, help_text='Please capitalize the name', null=True, on_delete=django.db.models.deletion.CASCADE, to='colleges.residentialarea')),
            ],
        ),
        migrations.AddConstraint(
            model_name='college',
            constraint=models.UniqueConstraint(fields=('college_name', 'state_province', 'country'), name='college_alt_key'),
        ),
        migrations.AddConstraint(
            model_name='residentialarea',
            constraint=models.UniqueConstraint(fields=('college', 'res_hall_name'), name='resArea_alt_key'),
        ),
        migrations.AddConstraint(
            model_name='dorms',
            constraint=models.UniqueConstraint(fields=('college', 'dorm_name'), name='dorms_alt_key'),
        ),
    ]