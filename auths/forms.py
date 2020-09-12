from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from .models import *



class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=5,required=True, label='Şifre',
                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    password_confirm = forms.CharField(max_length=5, label='Şifre(Tekrar)',
                widget=forms.PasswordInput(attrs={'class':'form-control'}))

    gender = forms.ChoiceField(required=True, choices=UserProfile.GENDER,
                label='Cinsiyetiniz')


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'gender',
            'email',
            'password',
            'password_confirm'
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class' : 'form-control'}

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


        #passwordlar eşmesini kontrol ediyoruz:
    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password','Parolalar eşleşmiyor.')
            self.add_error('password_confirm','Parolalar eşleşmiyor')

        #burda bir kullanının bir email ile giriş yapabilmesi için denetliyoruz
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email sistemde kayıtlı')
        
        return email

        #user_name leride kontrol edelim: aynı kullanıcı adı olmasın
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı sistemde mevcut')

        return username




class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Kullanıcı Adı veya e-mail adresinizi giriniz',
                    widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Şifre',
                    widget=forms.PasswordInput(attrs={'class':'fom-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError('<b> Hatalı kullanıcı adı veya şifre girdiniz! </b>')

    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if re.match("[^@]+@[^@]+\.[^@]+", username):
            users =  User.objects.filter(email__iexact = username)

            if len(users) > 0 and len(users) == 1:
                return users.first().username
        
        return username

