# Generated by Django 2.2.4 on 2019-08-18 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("peering", "0050_auto_20190806_2159")]

    operations = [
        migrations.RenameField(
            model_name="autonomoussystem", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="bgpgroup", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="community", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="directpeeringsession", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="internetexchange", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="internetexchangepeeringsession",
            old_name="comment",
            new_name="comments",
        ),
        migrations.RenameField(
            model_name="router", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="routingpolicy", old_name="comment", new_name="comments"
        ),
        migrations.RenameField(
            model_name="template", old_name="comment", new_name="comments"
        ),
    ]