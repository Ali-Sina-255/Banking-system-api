from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import NextOfKin, Profile


class ProfileAdminForm(forms.ModelForm):
    photo = CloudinaryFileField(
        options={"crop": "thumb", "width": 200, "height": 200, "folder": "bank_photo"},
        required=False,
    )


class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields = ["first_name", "last_name", "relationship", "phone_number", "is_primary"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = [
        "user",
        "full_name",
        "phone_number",
        "email",
        "employment_status",
        "photo_preview",
    ]
    list_display_links = ["user"]
    list_filter = ["gender", "employment_status", "country"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
    ]
    readonly_fields = ["user"]

    fieldsets = (
        (
            _("Personal Information"),
            {
                "fields": (
                    "user",
                    "photo",
                    "id_photo",
                    "signature_photo",
                    "title",
                    "gender",
                    "date_of_birth",
                    "marital_status",
                ),
            },
        ),
        (
            _("Contact Information"),
            {
                "fields": ("phone_number", "address", "city", "country"),
            },
        ),
        (
            _("Identification"),
            {
                "fields": (
                    "means_of_identification",
                    "id_issue_date",
                    "id_expiry_date",
                    "password_number",
                ),
            },
        ),
        (
            _("Employment Information"),
            {
                "fields": (
                    "employment_status",
                    "employer_name",
                    "annual_income",
                    "date_of_employment",
                    "employer_city",
                    "employer_state",
                ),
            },
        ),
    )

    inlines = [NextOfKinInline]

    def full_name(self, obj):
        return (
            obj.user.get_full_name()
            if hasattr(obj.user, "get_full_name")
            else f"{obj.user.first_name} {obj.user.last_name}"
        )

    full_name.short_description = _("Full Name")

    def email(self, obj):
        return obj.user.email

    email.short_description = _("Email")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="200" style="object-fit: cover;" />',
                obj.photo.url,
            )
        return _("No Photo Yet")

    photo_preview.short_description = _("Photo Preview")


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ["full_name", "title", "profile"]
    list_filter = ["is_primary", "relationship"]
    search_fields = ["first_name", "last_name", "profile__user__email"]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = _("Full Name")
