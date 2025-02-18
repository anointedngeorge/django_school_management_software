# Generated by Django 4.2.11 on 2024-05-19 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myschool', '0003_alter_sections_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parents',
            name='code',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='parents',
            name='permissions',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='students',
            name='permissions',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='teachers',
            name='code',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='teachers',
            name='permissions',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='classes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_classes', to='myschool.classes'),
        ),
        migrations.AlterField(
            model_name='students',
            name='sections',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_sections', to='myschool.sections'),
        ),
    ]
