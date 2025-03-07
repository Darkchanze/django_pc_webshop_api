# Generated by Django 5.1.4 on 2025-03-07 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('manufacturer', models.CharField(max_length=70)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('USD', 'US-Dollar'), ('GBP', 'British Pound')], default='EUR', max_length=3)),
                ('description', models.TextField()),
                ('technical_details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('is_customized', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Pc_Components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pc_components.component')),
                ('pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pc_components.pc')),
            ],
        ),
        migrations.AddField(
            model_name='pc',
            name='components',
            field=models.ManyToManyField(through='pc_components.Pc_Components', to='pc_components.component'),
        ),
    ]
