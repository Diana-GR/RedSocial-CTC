# Generated by Django 5.1 on 2024-08-27 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_rename_date_completed_task_datecompleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="datecompleted",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
