from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .forms import ExpSmoothingParamsForm, ExpSmoothingMetricsForm, GRUParamsForm, GRUMetricsForm
from data_app.models import ExpSmoothingParams, ExpSmoothingMetrics, GRUParams, GRUMetrics
from scripts import exp_sm_model, data_interpolate, request_data, GRU_model


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account activation'
            message = render_to_string('users/activate_acc.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'An email with a confirmation has been sent to your email address.')
            return render(request, 'users/register.html', {'form': form})
        else:
            errors = form.errors
            return render(request, 'users/register.html', {'form': form, 'errors': errors})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('signin')
    else:
        return HttpResponse('Activation link is invalid!')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            # user = authenticate(username=cd['username'], password=cd['password'])
            user = User.objects.get(username=cd['username'])
            user_check = user.check_password(cd['password'])
            if user_check:
                if user.user_type == 'client':
                    if user.is_active:
                        login(request, user)
                        return redirect('chart')
                    else:
                        messages.error(request, 'Please activate your account!')
                        return redirect('signin')
                elif user.user_type == 'analyst':
                    login(request, user)
                    return redirect('analyst_panel')
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Incorrect username or password'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def analyst_page_view(request):
    if request.user.user_type == 'client':
        messages.warning(request, "У вас недостаточно прав для доступа на эту страницу.")
        return redirect('signin')
    exp_smoothing_params_instance = ExpSmoothingParams.objects.first()
    exp_smoothing_metrics_instance = ExpSmoothingMetrics.objects.first()
    gru_params_instance = GRUParams.objects.first()
    gru_metrics_instance = GRUMetrics.objects.first()

    if request.method == 'POST':
        if "save_button" in request.POST:
            form_exp_smoothing_params = ExpSmoothingParamsForm(request.POST, instance=exp_smoothing_params_instance)
            form_exp_smoothing_metrics = ExpSmoothingMetricsForm(request.POST, instance=exp_smoothing_metrics_instance)
            form_gru_params = GRUParamsForm(request.POST, instance=gru_params_instance)
            form_gru_metrics = GRUMetricsForm(request.POST, instance=gru_metrics_instance)

            if form_exp_smoothing_params.is_valid():
                form_exp_smoothing_params.save()

            if form_exp_smoothing_metrics.is_valid():
                form_exp_smoothing_metrics.save()

            if form_gru_params.is_valid():
                form_gru_params.save()

            if form_gru_metrics.is_valid():
                form_gru_metrics.save()
            return redirect('analyst_panel')
        try:
            if 'get_data' in request.POST:
                request_data.run()
                messages.success(request, 'Данные получены.')
                return redirect('analyst_panel')
            if 'data_processing' in request.POST:
                data_interpolate.run()
                messages.success(request, 'Данные обработаны.')
                return redirect('analyst_panel')
            if 'exp_button' in request.POST:
                exp_sm_model.run()
                messages.success(request, 'Модель обучена.')
                return redirect('analyst_panel')
            if 'gru_button' in request.POST:
                GRU_model.run()
                messages.success(request, 'Модель обучена.')
                return redirect('analyst_panel')
        except:
            messages.error(request, 'Что-то пошло не так.')
            return redirect('analyst_panel')
    else:
        form_exp_smoothing_params = ExpSmoothingParamsForm(instance=exp_smoothing_params_instance)
        form_exp_smoothing_metrics = ExpSmoothingMetricsForm(instance=exp_smoothing_metrics_instance)
        form_gru_params = GRUParamsForm(instance=gru_params_instance)
        form_gru_metrics = GRUMetricsForm(instance=gru_metrics_instance)

    return render(request, 'users/analyst_panel.html', {
        'form_exp_smoothing_params': form_exp_smoothing_params,
        'form_exp_smoothing_metrics': form_exp_smoothing_metrics,
        'form_gru_params': form_gru_params,
        'form_gru_metrics': form_gru_metrics,
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('signin')


def welcome_page(request):
    return render(request, 'users/welcome_page.html')
