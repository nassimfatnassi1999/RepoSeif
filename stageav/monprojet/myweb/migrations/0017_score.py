# Generated by Django 4.2.4 on 2023-08-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0016_alter_user_encadrant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.user')),
            ],
        ),
    ]
