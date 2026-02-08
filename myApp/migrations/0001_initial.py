from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Education",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("institution", models.CharField(blank=True, max_length=200)),
                ("date_range", models.CharField(max_length=60)),
                ("description", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("issuer", models.CharField(max_length=120)),
                ("issued_date", models.CharField(max_length=60)),
                ("file_path", models.CharField(blank=True, max_length=255)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(max_length=160)),
                ("short_description", models.CharField(max_length=280)),
                ("long_description", models.TextField()),
                ("tech_stack", models.JSONField(blank=True, default=list)),
                ("highlights", models.JSONField(blank=True, default=list)),
                ("image_path", models.CharField(blank=True, max_length=255)),
                ("demo_url", models.URLField(blank=True)),
                ("source_code_price_inr", models.PositiveIntegerField(default=0)),
                ("is_featured", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
    ]
