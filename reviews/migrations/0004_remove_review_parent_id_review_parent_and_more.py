# Generated by Django 4.2.14 on 2024-08-06 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0003_alter_review_restaurant"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="parent_id",
        ),
        migrations.AddField(
            model_name="review",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="reviews.review",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="decommend_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="review",
            name="recommend_count",
            field=models.IntegerField(default=0),
        ),
    ]
