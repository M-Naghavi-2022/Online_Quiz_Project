# Generated by Django 4.0.4 on 2022-05-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_quiz_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(choices=[('choice_a', 'choice a'), ('choice_b', 'choice b'), ('choice_c', 'choice c'), ('choice_d', 'choice d')], max_length=8),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='result',
            field=models.JSONField(default={'blank_ans': 0, 'correct_ans': 0, 'total_score': 0, 'wrong_ans': 0}),
        ),
        migrations.AlterField(
            model_name='quizitem',
            name='user_answer',
            field=models.CharField(choices=[('choice_a', 'choice a'), ('choice_b', 'choice b'), ('choice_c', 'choice c'), ('choice_d', 'choice d')], max_length=8),
        ),
    ]
