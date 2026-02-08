from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0003_alter_certificate_drive_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="projects/"),
        ),
    ]
