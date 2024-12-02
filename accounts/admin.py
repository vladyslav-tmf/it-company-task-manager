from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class WorkerAdmin(UserAdmin):
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (["Personal info", {"fields": ["email", "first_name", "last_name"]}],)
    )
    search_fields = ["username", "first_name", "last_name", "position__name"]
    list_filter = ["position"]
    list_select_related = ["position"]

    def get_form(self, request, obj=None, **kwargs):
        """
        Retrieves and customizes a form for a given request and object. The method
        obtains the form through the superclass method and modifies it by making
        certain fields required, as defined by the "mark_fields_as_required" method.
        """
        custom_form = super().get_form(request, obj, **kwargs)
        self.mark_fields_as_required(custom_form)
        return custom_form

    @staticmethod
    def mark_fields_as_required(form):
        """
        Sets the required property to True for specified fields in a form. This method
        ensures that the "first_name", "last_name", and "email" fields are marked as
        required, enforcing user input for these fields upon submission.
        """
        for field in WorkerAdmin.REQUIRED_FIELDS:
            form.base_fields[field].required = True
