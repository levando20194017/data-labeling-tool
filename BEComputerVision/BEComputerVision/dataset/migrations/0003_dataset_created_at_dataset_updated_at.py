# Generated by Django 4.2.15 on 2024-09-28 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataset", "0002_alter_dataset_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default="2024-01-01 00:00:00"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dataset",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
