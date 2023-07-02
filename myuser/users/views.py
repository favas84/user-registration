import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import RegistrationForm, LoginForm


# Create a base view class that includes the common behavior
class RoleRestrictedView(LoginRequiredMixin, TemplateView):
    allowed_roles = []  # List of allowed roles for the view

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.role not in self.allowed_roles:
            raise PermissionDenied(
                "You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    @staticmethod
    def save_user_data(form):
        data = form.cleaned_data
        try:
            name = data['name']
            email = data['email']
            role = data['role']
            country = data['country']
            nationality = data['nationality']
            mobile = data['mobile']

            user = form.save(commit=False)
            user.username = email
            user.email = email
            user.first_name = name
            user.role = role
            user.country = country
            user.nationality = nationality
            user.mobile = mobile
            user.save()

            return user
        except Exception:
            logging.error('Not able to save user data', exc_info=True)
            pass
        return

    def authenticate_and_login_user(self, user, password):
        user = authenticate(username=user.email, password=password)
        if user is not None:
            login(self.request, user)

    def post(self, request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = self.save_user_data(form)
                self.authenticate_and_login_user(user, form.cleaned_data[
                    'password1'])
                form.save()
                return redirect(self.success_url)
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a page based on the user's role
                if user.role == 'student':
                    return redirect('student')
                elif user.role == 'staff':
                    return redirect('staff')
                elif user.role == 'admin':
                    return redirect('admin')
                elif user.role == 'editor':
                    return redirect('editor')
        else:
            # Form is invalid, show the errors
            return render(request, 'login.html', {'form': form})


class StudentView(RoleRestrictedView):
    template_name = 'student.html'
    allowed_roles = ['student']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class StaffView(RoleRestrictedView):
    template_name = 'staff.html'
    allowed_roles = ['staff']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AdminView(RoleRestrictedView):
    template_name = 'admin.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EditorView(RoleRestrictedView):
    template_name = 'editor.html'
    allowed_roles = ['editor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
