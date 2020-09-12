from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from blog.decorators import *
from django.contrib.auth.models import User
from .models import *



# @anonymous_required
def register(request):

    # if not request.user.is_anonymous():
    #     return HttpResponseRedirect(reverse('post-list'))

    form = RegisterForm(data=request.POST or None)
    
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        gender = form.cleaned_data.get('gender')
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, gender=gender)

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, 'Tebrikler Kaydınız Başarıyla Gerçekleşti.')

                return HttpResponseRedirect(reverse('post-list'))
                # reverse ile post-list sayfamıza yönlendirdik.

    return render(request, 'auths/register.html', context={'form':form})



# @anonymous_required
def user_login(request):

    form = LoginForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username,password=password)
        
        if user:

            if user.is_active:
                login(request,user)
                msg = '<b> Merhaba %s siteye hoşgeldiniz. </b>' %(username)
                messages.success(request, msg)

            return HttpResponseRedirect(reverse('post-list'))


    return render(request, 'auths/login.html', context={'form':form})



def user_logout(request):
    username = request.user.username
    logout(request)

    msg = '<b> Tekrar görüşmek üzere %s. </b>' %(username)
    messages.success(request,msg)

    return HttpResponseRedirect(reverse('post-list'))



def user_profile(request,username):
    user = get_object_or_404(User, username=username)
    return render(request,'',context={'user':user})


