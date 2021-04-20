# Generated by Django 3.1.7 on 2021-03-21 17:43

import django.db.models.deletion
import netfields.fields
import taggit.managers
from django.db import migrations, models

import net.fields
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("peeringdb", "0015_auto_20210227_1258"),
        ("utils", "0007_auto_20200805_2322"),
    ]

    operations = [
        migrations.CreateModel(
            name="Connection",
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
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "state",
                    models.CharField(
                        choices=[("enabled", "Enabled"), ("disabled", "Disabled")],
                        default="enabled",
                        max_length=20,
                    ),
                ),
                (
                    "vlan",
                    net.fields.VLANField(blank=True, null=True, verbose_name="VLAN"),
                ),
                (
                    "ipv6_address",
                    netfields.fields.InetAddressField(
                        blank=True,
                        max_length=39,
                        null=True,
                        validators=[utils.validators.AddressFamilyValidator(6)],
                    ),
                ),
                (
                    "ipv4_address",
                    netfields.fields.InetAddressField(
                        blank=True,
                        max_length=39,
                        null=True,
                        validators=[utils.validators.AddressFamilyValidator(4)],
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("interface", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                (
                    "internet_exchange_point",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="peering.internetexchange",
                    ),
                ),
                (
                    "peeringdb_netixlan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="peeringdb.networkixlan",
                    ),
                ),
                (
                    "router",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="peering.router",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="utils.TaggedItem",
                        to="utils.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
