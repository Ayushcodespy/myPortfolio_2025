from django.db import migrations, models


def backfill_source_code_urls(apps, schema_editor):
    Project = apps.get_model("myApp", "Project")
    updates = {
        "arya-z-tech": "/static/source_code/arya-z-tech.zip",
        "old-portfolio": "/static/source_code/portfolio01.zip",
        "new-portfolio": "/static/source_code/myPortfolio_2025.zip",
        "agro-trade-portal": "/static/source_code/agro-trade-portal.zip",
    }
    for slug, url in updates.items():
        Project.objects.filter(slug=slug, source_code_url="").update(source_code_url=url)


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0006_alter_certificate_drive_link_alter_project_demo_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="source_code_url",
            field=models.CharField(
                blank=True,
                help_text="Public source code URL, e.g. https://... or /static/source_code/project.zip",
                max_length=500,
            ),
        ),
        migrations.RunPython(backfill_source_code_urls, migrations.RunPython.noop),
    ]
