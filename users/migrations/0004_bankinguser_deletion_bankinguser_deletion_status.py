# Generated by Django 5.0.2 on 2024-03-13 16:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_bankinguser_pd_modification_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankinguser",
            name="deletion",
            field=models.CharField(
                blank=True,
                choices=[("yes", "Yes"), ("no", "No")],
                default="no",
                max_length=128,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bankinguser",
            name="deletion_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("pending", "Waiting for Approval"),
                    ("rejected", "Rejected"),
                    ("approved", "Approved"),
                ],
                max_length=128,
                null=True,
            ),
        ),
    ]
