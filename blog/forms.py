from django.db import models
from django import forms
from .models import *


banned_email_list = [
    'ahmet@hotmail.com',
    'grkm-50@hotmail.com',
    'teoman@hotmail.com',
]

class IletisimForm(forms.Form):
    konu = forms.CharField(max_length=50, label='Konu')
    isim = forms.CharField(max_length=50, label='İsim', required=False)
    soyisim = forms.CharField(max_length=50, label='Soyisim', required=False)
    email = forms.EmailField(max_length=70, label='E-mail', required=True)
    email2 = forms.EmailField(max_length=70, label='E-mail Doğrulama', required=True)
    icerik = forms.CharField(max_length=1000, label='İçerik')

    def __init__(self, *args, **kwargs):

        super(IletisimForm, self).__init__(*args, **kwargs)
        for field in self.fields:

            self.fields[field].widget.attrs = {'class':'form-control'}

        self.fields['icerik'].widget = forms.Textarea(attrs = {'class':'form-control'})
        self.fields['konu'].widget = forms.Select(attrs = {'class':'form-control'})


    def clean_isim(self):
        ad = self.cleaned_data.get('isim')

        if ad == 'ahmet':
            raise forms.ValidationError("Lütfen 'ahmet' dışında bir kullanıcı girin.")
        return ad


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email in banned_email_list:
            raise forms.ValidationError('Lütfen farklı bir e-mail adresi girin.')

        return email


    # şimdi email1-ile 2 birbirine eşit degilse hata versin
    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            self.add_error('email','Emailler Eşleşmedi')
            self.add_error('email2','Emailler Eşleşmedi')



class BlogForm(forms.ModelForm):
    class Meta: # class meta aslında classın settings i
        #hangi modelimde çagırıcaksam onu çagırıyoruz:
        model = Blog

        fields = [
            'title',
            'content',
            'yayin_taslak',
            'kategoriler',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}

        self.fields['content'].widget.attrs['rows'] = 10
        # bunu yapmamızdaki amaç html sayfasında içerik kutusunun büyük gözükmesi

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if len(content) < 250:
            uzunluk = len(content)
            msg = 'Lütfen en az 250 karakter giriniz, Girilen karakter sayısı: (%s)'%(uzunluk)
            raise forms.ValidationError(msg)
        
        return content

class PostSorguForm(forms.Form):
    YAYIN_TASLAK = (('all','HEPSİ'),('yayin','YAYIN'),('taslak','TASLAK'))

    search = forms.CharField(required=False,max_length=500,widget=forms.TextInput(attrs={'placeholder':'Ara.','class':'form-control'}))

    taslak_yayin = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}),
                                     choices=YAYIN_TASLAK, required=False)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'isim',
            'soyisim',
            'email',
            'icerik',
        ]
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class' : 'form-control'}
            