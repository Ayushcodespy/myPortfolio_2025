from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0002_rename_certificate_drive_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificate",
            name="drive_link",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
