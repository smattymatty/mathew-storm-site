# Generated by Django 5.2.1 on 2025-06-11 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_alter_question_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorialtitle',
            name='name',
            field=models.CharField(blank=True, help_text='A human-readable name for the tutorial', max_length=255),
        ),
        migrations.AlterField(
            model_name='tutorialtitle',
            name='title_id_slug',
            field=models.SlugField(help_text='The unique slug for the tutorial title', max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='QuestionStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('total_successes', models.PositiveIntegerField(default=0)),
                ('total_failures', models.PositiveIntegerField(default=0)),
                ('success_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('average_time_seconds', models.PositiveIntegerField(default=0)),
                ('skip_count', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='questions.question')),
            ],
            options={
                'verbose_name': 'Question Statistics',
                'verbose_name_plural': 'Question Statistics',
            },
        ),
        migrations.CreateModel(
            name='TutorialStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('total_completions', models.PositiveIntegerField(default=0)),
                ('completion_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('average_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('average_completion_time_minutes', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('tutorial_title', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='questions.tutorialtitle')),
            ],
            options={
                'verbose_name': 'Tutorial Statistics',
                'verbose_name_plural': 'Tutorial Statistics',
            },
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_answer', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], max_length=1)),
                ('is_correct', models.BooleanField()),
                ('time_spent_seconds', models.PositiveIntegerField(default=0)),
                ('attempt_number', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='questions.question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['user', 'question'], name='questions_q_user_id_d71862_idx'), models.Index(fields=['question', 'is_correct'], name='questions_q_questio_7b90a5_idx'), models.Index(fields=['created_at'], name='questions_q_created_2f1280_idx')],
            },
        ),
    ]
