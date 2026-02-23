from django.db import models


class Education(models.Model):
    title = models.CharField(max_length=120)
    institution = models.CharField(max_length=200, blank=True)
    date_range = models.CharField(max_length=60)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title} ({self.date_range})"


class Certificate(models.Model):
    title = models.CharField(max_length=160)
    issuer = models.CharField(max_length=120)
    issued_date = models.CharField(max_length=60)
    drive_link = models.CharField(
        max_length=255,
        blank=True,
        help_text="Drive/public URL or static path, e.g. certificates/MyCert.pdf",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Project(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    short_description = models.CharField(max_length=280)
    long_description = models.TextField()
    tech_stack = models.JSONField(
        default=list,
        blank=True,
        help_text='JSON list, e.g. ["Django", "HTML", "CSS"]',
    )
    highlights = models.JSONField(
        default=list,
        blank=True,
        help_text='JSON list, e.g. ["Responsive UI", "Fast load time"]',
    )
    image = models.FileField(upload_to="projects/", blank=True, null=True)
    source_code_zip = models.FileField(upload_to="project_zips/", blank=True, null=True)
    image_path = models.CharField(
        max_length=255,
        blank=True,
        help_text="Static path or full URL, e.g. images/projects/project.png",
    )
    source_code_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Public source code URL, e.g. https://... or /static/source_code/project.zip",
    )
    demo_url = models.URLField(blank=True, help_text="Live link URL")
    source_code_price_inr = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
