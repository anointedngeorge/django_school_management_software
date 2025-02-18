# Generated by Django 4.2.11 on 2024-05-17 17:23

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('school_name', models.CharField(max_length=100)),
                ('school_phone', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(choices=[(True, 'Active'), (False, 'Suspended')], default=True)),
                ('school_address', models.TextField()),
            ],
            options={
                'verbose_name': 'school',
                'verbose_name_plural': 'Schools',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='schools.schools')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
