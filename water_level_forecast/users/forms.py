from django import forms
from django.contrib.auth.forms import UserCreationForm

from data_app.models import ExpSmoothingParams, ExpSmoothingMetrics, GRUParams, GRUMetrics
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)


class ExpSmoothingParamsForm(forms.ModelForm):
    class Meta:
        model = ExpSmoothingParams
        fields = '__all__'


class ExpSmoothingMetricsForm(forms.ModelForm):
    class Meta:
        model = ExpSmoothingMetrics
        fields = '__all__'


class GRUParamsForm(forms.ModelForm):
    class Meta:
        model = GRUParams
        fields = '__all__'


class GRUMetricsForm(forms.ModelForm):
    class Meta:
        model = GRUMetrics
        fields = '__all__'
