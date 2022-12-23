# Generated by Django 4.1.4 on 2022-12-22 11:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_alter_student_balance_alter_student_student_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.UUIDField(default=uuid.uuid4)),
                ('price', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.student')),
            ],
        ),
    ]