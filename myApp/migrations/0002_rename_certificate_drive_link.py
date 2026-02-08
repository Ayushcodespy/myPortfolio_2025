from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="certificate",
            old_name="file_path",
            new_name="drive_link",
        ),
        migrations.AlterField(
            model_name="certificate",
            name="drive_link",
            field=models.URLField(blank=True),
        ),
    ]
