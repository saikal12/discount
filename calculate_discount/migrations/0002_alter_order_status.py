# Generated by Django 5.1.3 on 2024-12-08 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculate_discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]