# Generated by Django 4.2.8 on 2024-05-20 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('IMaster', '0002_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_topics', models.ManyToManyField(related_name='completed_by_students', to='IMaster.topic')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_progress', to='IMaster.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
    ]
