from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator

User = get_user_model()

ROLE_CHOICES = (
    ('student', 'Student'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
    ('editor', 'Editor'),
)


class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=75, required=True)
    email = forms.EmailField(max_length=200, validators=[EmailValidator])
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    country = forms.CharField(max_length=100)
    nationality = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('name', 'email', 'role', 'country', 'nationality', 'mobile')

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit():
            raise forms.ValidationError(
                "Mobile number should contain only digits."
            )
        return mobile

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email', validators=[EmailValidator])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again.")

        return cleaned_data

    def clean_username(self):
        email = self.cleaned_data['username'].lower()
        try:
            User.objects.get(
                email=email, is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError("The email address you entered does "
                                        "not match any account")
        return email
