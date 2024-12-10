from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (["Personal info", {"fields": ["email", "first_name", "last_name"]}],)
    )
    search_fields = ["username", "first_name", "last_name", "position__name"]
    list_filter = ["position"]
    list_select_related = ["position"]

    def get_form(self, request, obj=None, **kwargs):
        custom_form = super().get_form(request, obj, **kwargs)
        for field_name in ["first_name", "last_name", "email"]:
            custom_form.base_fields[field_name].required = True
        return custom_form
