from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tasks.models import Position, Task, TaskType

MAX_LENGTH = 255


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), widget=forms.CheckboxSelectMultiple
    )
    deadline = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Deadline")
    priority = forms.ChoiceField(choices=Task.Priority.choices, label="Priority", initial=Task.Priority.STANDARD)

    class Meta:
        model = Task
        fields = [
            "name",
            "task_type",
            "is_completed",
            "description",
            "deadline",
            "priority",
            "assignees",
        ]


class TaskTypeForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"))
    class Meta:
        model = TaskType
        fields = ["name"]


class PositionForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"))
    class Meta:
        model = Position
        fields = ["name"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=MAX_LENGTH,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Search by task name")}),
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=MAX_LENGTH,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Search by task type name")}),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=MAX_LENGTH,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Search by position name")}),
    )
