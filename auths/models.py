from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER = ((None, 'Cinsiyet Seçiniz'),('erkek','ERKEK'),('kadın','KADIN'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=False, verbose_name='Kullanıcı')
    bio = models.TextField(max_length=1000, verbose_name='Hakkımda', blank=True, null=True)
    profile_photo = models.ImageField(null=True, blank=True, verbose_name='Profil Fotoğrafı')
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    gender = models.CharField(choices = GENDER, blank=False, null=True, verbose_name='Cinsiyet', max_length=6)


    class Meta:
        verbose_name_plural = 'Kullanıcı Profilleri'

    def get_screen_name(self):
        user = self.user

        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def __str__(self):
        return '%s Profil' % (self.get_screen_name())
