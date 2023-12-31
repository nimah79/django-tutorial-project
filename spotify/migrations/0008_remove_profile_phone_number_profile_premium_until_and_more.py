# Generated by Django 4.2.4 on 2023-11-28 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("spotify", "0007_like_created_at_like_updated_at_rate_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="profile",
            name="premium_until",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(("app_label", "spotify"), ("model", "subscription")),
                    models.Q(("app_label", "spotify"), ("model", "voucher")),
                    _connector="OR",
                ),
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
    ]
