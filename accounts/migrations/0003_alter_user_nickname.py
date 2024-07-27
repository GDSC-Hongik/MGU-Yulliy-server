# Generated by Django 4.2.14 on 2024-07-27 04:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                error_messages={"unique": "이미 사용 중인 닉네임입니다."},
                max_length=20,
                null=True,
                unique=True,
            ),
        ),
    ]