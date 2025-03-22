from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from random import randint
from django.utils.crypto import get_random_string
from uuid import uuid4
from .forms import LoginForm, RegisterForm, CheckOtpForm, AddressCreationForm
import ghasedak_sms

from .models import Otp, User

sms_api = ghasedak_sms.Ghasedak(api_key='4c9f71973c64764fdbb0ffea902bdc4734d4ce0cabeb2f63ecfe39758abf103eUJy3ckc7JtgEYEgC')

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(selfself,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'phone or password is invalid')
        else:
            form.add_error('phone', 'phone or password is invalid')

        return render(request, 'account/login.html', {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/otp_login.html', {'form': form})
    def post(selfself, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            oldotpcommand = ghasedak_sms.SendOldOtpInput(
                send_date='',
                receptors=[
                    ghasedak_sms.SendOtpReceptorDto(
                        mobile=cd['phone'],
                        # client_reference_id='client_ref_id'
                    )
                ],
                template_name='Ghasedak',
                param1=randcode,
                is_voice=False,
                udh=False
            )

            response = sms_api.send_otp_sms_old(oldotpcommand)

            print(response)
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error('phone', 'phone or password is invalid')

        return render(request, 'account/otp_login.html', {'form': form})

class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html',{'form': form})
    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user)
                otp.delete()
                return redirect('/')
        else:
            form.add_error('phone', 'phone or password is invalid')

        return render(request, 'account/check_otp.html', {'form': form})

class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page=request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return render(request,'account/add_address.html',{'form': form})
    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html',{'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')