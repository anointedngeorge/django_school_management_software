# Generated by Django 4.2.11 on 2024-07-01 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myschool', '0013_resultcomment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultcomment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_comment_related', to='myschool.students'),
        ),
    ]
