from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views import View, generic
from django.views.generic import FormView

from accounts.forms import (
    WorkerRegisterForm,
    WorkerSearchForm,
    WorkerUpdateForm,
)
from accounts.services.email_service import EmailService
from accounts.services.token_service import account_activation_token
from tasks.models import Task

User = get_user_model()


class WorkerRegisterView(FormView):
    form_class = WorkerRegisterForm
    template_name = "registration/register.html"

    def _update_field_widget_attributes(
        self, field_name: str, placeholder: str
    ) -> None:
        field = self.form.fields[field_name]
        field.widget.attrs.update(
            {
                "placeholder": placeholder,
                "class": "form-control",
            }
        )

    def get_form(self, form_class=WorkerRegisterForm) -> WorkerRegisterForm:
        self.form = super().get_form(form_class)

        self._update_field_widget_attributes("username", _("Username"))
        self._update_field_widget_attributes("password1", _("Password"))
        self._update_field_widget_attributes("password2", _("Password check"))

        return self.form

    def form_valid(self, form: WorkerRegisterForm) -> HttpResponseRedirect:
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        domain = get_current_site(self.request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        email_service = EmailService()
        email_service.send_activation_email(
            username=user.username,
            domain=domain,
            uid=uid,
            to_email=user.email,
            token=token,
        )

        messages.info(
            self.request, _("Please confirm your activation link in your email.")
        )

        return redirect("accounts:login")


class WorkerActivateView(View):
    @staticmethod
    def get(request: HttpRequest, uid: str, token: str) -> HttpResponseRedirect:
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and user.is_active:
            messages.info(request, _("Your account is already activated."))
            return redirect("accounts:login")

        elif user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                _(
                    "Thank you for your email confirmation. Now you can sign in to your account."
                ),
            )
            return redirect("accounts:login")

        messages.error(
            request, _("Activation link is invalid or has already been used.")
        )
        return redirect("accounts:register")


class WorkerLoginView(FormView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("tasks:index")

    def get_form(self, form_class=AuthenticationForm) -> AuthenticationForm:
        form = super().get_form(form_class)
        self._customize_field(form, "username", _("Username"))
        self._customize_field(form, "password", _("Password"))
        return form

    @staticmethod
    def _customize_field(
        form: AuthenticationForm, field_name: str, placeholder: str
    ) -> None:
        field = form.fields[field_name]
        field.label = ""
        field.widget.attrs.update(
            {
                "placeholder": placeholder,
                "class": "form-control",
            }
        )

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)
            return super().form_valid(form)

        else:
            form.add_error(None, _("Invalid credentials"))
            return self.form_invalid(form)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5
    context_object_name = "workers"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm()

        return context

    def get_queryset(self) -> QuerySet[User]:
        username = self.request.GET.get("username")

        if username:
            return User.objects.filter(username__icontains=username).select_related(
                "position"
            )

        return User.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.select_related("position")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        tasks = worker.tasks.all()
        context["completed_tasks"] = [task for task in tasks if task.is_completed]
        context["pending_tasks"] = [task for task in tasks if not task.is_completed]

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("accounts:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("accounts:worker-list")


class ToggleAssignToTaskView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponseRedirect:
        task = get_object_or_404(Task, id=pk)
        worker = request.user

        if task in worker.tasks.all():
            worker.tasks.remove(task)

        else:
            worker.tasks.add(task)

        return HttpResponseRedirect(reverse_lazy("tasks:task-detail", args=[pk]))
