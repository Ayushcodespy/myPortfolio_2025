from django.contrib import admin

from .models import Certificate, Education, Project


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "date_range", "order")
    list_editable = ("order",)
    search_fields = ("title", "institution")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issued_date", "order")
    list_editable = ("order",)
    search_fields = ("title", "issuer")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_featured", "source_code_price_inr", "order")
    list_editable = ("is_featured", "order", "source_code_price_inr")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
