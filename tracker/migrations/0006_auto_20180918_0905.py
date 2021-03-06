# Generated by Django 2.1 on 2018-09-18 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20180917_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='task_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Codes'),
        ),
    ]
