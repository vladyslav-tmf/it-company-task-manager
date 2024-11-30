from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Position

User = get_user_model()


class WorkerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(), help_text="Please choose a position", required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "position")


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "position"]


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255, label="", required=False, widget=forms.TextInput(attrs={"placeholder": "Search by Username"})
    )
