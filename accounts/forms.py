from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from tasks.models import Position

MAX_LENGTH = 255
User = get_user_model()


class WorkerRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Email"),
            }
        ),
    )
    first_name = forms.CharField(
        max_length=MAX_LENGTH,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("First name"),
            }
        ),
    )
    last_name = forms.CharField(
        max_length=MAX_LENGTH,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Last name"),
            }
        ),
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        help_text=_("Please choose a position"),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "position"]


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=MAX_LENGTH,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Search by Username")}),
    )
