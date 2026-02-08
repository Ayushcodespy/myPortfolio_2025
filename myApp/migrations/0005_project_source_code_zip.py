from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0004_project_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="source_code_zip",
            field=models.FileField(blank=True, null=True, upload_to="project_zips/"),
        ),
    ]
