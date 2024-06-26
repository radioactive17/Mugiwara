# Generated by Django 5.0.2 on 2024-03-09 20:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BankingUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "usertype",
                    models.CharField(
                        choices=[
                            ("iu_re", "Regular Employee"),
                            ("iu_sm", "System Manager"),
                            ("iu_sa", "System Administrator"),
                            ("eu_cust", "Customer"),
                            ("eu_mo", "Merchant/Organization"),
                        ],
                        max_length=256,
                    ),
                ),
                ("dob", models.DateField(blank=True, default=None, null=True)),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "street_address",
                    models.CharField(
                        blank=True, default=None, max_length=512, null=True
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, default=None, max_length=128, null=True
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, default=None, max_length=128, null=True
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(
                        blank=True, default=None, max_length=10, null=True
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                ("account_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "pd_modification_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("pending", "Waiting for approval"),
                            ("rejected", "Rejected"),
                            ("approved", "Approved"),
                        ],
                        max_length=128,
                        null=True,
                    ),
                ),
                ("pd_modified", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_handler",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="internal_user",
                        to="users.bankinguser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("account_number", models.AutoField(primary_key=True, serialize=False)),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("sav", "Savings Account"),
                            ("check", "Checking Account"),
                        ],
                        max_length=128,
                    ),
                ),
                ("account_bal", models.BigIntegerField(default=0)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "account_status",
                    models.CharField(
                        choices=[("o", "Open"), ("c", "Close")],
                        default="o",
                        max_length=32,
                    ),
                ),
                ("closed_on", models.DateTimeField(blank=True, null=True)),
                (
                    "banking_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="banking_user",
                        to="users.bankinguser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transactions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.BigIntegerField()),
                (
                    "transaction_status",
                    models.CharField(
                        choices=[
                            ("pending", "Waiting for approval"),
                            ("rejected", "Rejected"),
                            ("approved", "Approved"),
                        ],
                        max_length=128,
                    ),
                ),
                ("initiated", models.DateTimeField(auto_now_add=True)),
                ("status_changed", models.DateTimeField(auto_now=True)),
                (
                    "from_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_account",
                        to="users.account",
                    ),
                ),
                (
                    "to_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_account",
                        to="users.account",
                    ),
                ),
                (
                    "transaction_handler",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction_handler",
                        to="users.bankinguser",
                    ),
                ),
            ],
        ),
    ]
