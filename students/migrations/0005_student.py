# Generated by Django 4.2.4 on 2023-10-01 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('student_number', models.CharField(max_length=10, unique=True)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
