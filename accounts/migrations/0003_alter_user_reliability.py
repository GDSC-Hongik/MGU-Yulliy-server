# Generated by Django 4.2.14 on 2024-08-01 11:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_user_groups_alter_user_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="reliability",
            field=models.SmallIntegerField(default=100),
        ),
    ]