# Generated by Django 3.1.7 on 2021-03-02 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StreamModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.coursemodel')),
            ],
        ),
        migrations.CreateModel(
            name='SubStreamModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.streammodel')),
            ],
        ),
    ]
