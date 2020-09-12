from django.db import models
from django.shortcuts import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify, safe
from uuid import uuid4
import os
from ckeditor.fields import RichTextField


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = '%s.%s'%(str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('blog',unique_id,new_name)
#instance: nesnenin kenidisini
# filename : dosyanın kendisi


 
class Kategori(models.Model):
    isim = models.CharField(max_length=20, verbose_name='Kategori İsim')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim    




class Blog(models.Model):

    YAYIN_TASLAK = ((None,'Lütfen Birini Seçiniz.'),('yayin','YAYIN'),('taslak','TASLAK'))
    # yayin : value'si oluyor
    # YAYIN görünürdeki görünümü

    title = models.CharField(max_length=100, verbose_name='Başlık', help_text='Başlığınızı Girin', blank=False, null=True)
    content = models.TextField(max_length=1000, verbose_name='İçerik', help_text='İçeriğinizi Girin', blank=False, null=True)
    date = models.DateField(auto_now_add=True,verbose_name='Zaman')
    slug = models.SlugField(null=True, unique=True, editable=False)
    kategoriler = models.ManyToManyField(to=Kategori, related_name='blog', help_text='Kategorilerinizi Seçiniz')
    image = models.ImageField(blank=True, default='default/python_django.jpg', upload_to=upload_to, verbose_name='Resim', null=True, help_text='Kapak Fotoğrafı Yükleyiniz')
    unique_id = models.CharField(max_length=100, editable=True, null=True)
    yayin_taslak = models.CharField(choices = YAYIN_TASLAK, max_length=6, null=True, blank=False)

    class Meta:
        verbose_name_plural = "Gönderiler"
        ordering = ['id']


    def __str__(self):
        return '%s' % (self.title)
        
    @classmethod
    def get_taslak_or_yayin(cls, taslak_yayin):
        return cls.objects.filter(yayin_taslak=taslak_yayin)

    def get_yayin_taslak_html(self):
        if self.yayin_taslak == 'taslak':
            return safe('<span class="label label-danger">{0}</span>'.format(self.get_yayin_taslak_display()))
            # veya böylede yazabiliriz:
            #return '<span class="label label-{0}">{1}</span>'.format('danger',self.get_yayin_taslak_display())
            
        return safe('<span class="label label-primary">{0}</span>'.format(self.get_yayin_taslak_display()))
        # return '<span class="label label-{0}">{1}</span>'.format('primary',self.get_yayin_taslak_display())


    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})


    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/python_django.jpg'


    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug

        while Blog.objects.filter(slug=new_slug).exists():
            # slug alanımdan aynısı varmı?
            # exist böyle değer var mı? True veya False dönüyor True işe döngüye giriyor
            sayi += 1 # bir sayıyı artır
            new_slug = "%s-%s" % (slug,sayi)
        
        slug = new_slug

        return slug


    def save(self, *args, **kwargs):

        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id

            self.slug = self.get_unique_slug()
        
        else:
            blog = Blog.objects.get(slug=self.slug) 

            if blog.title != self.title: # veri tabanındaki haliyle güncelleşmiş halini karşıalştırıyoruz
            # blog.title veri tabanındaki title, self.title ise daha kaydedilmemiş title
                self.slug = self.get_unique_slug()

        super(Blog, self).save(*args, **kwargs)

    def get_blog_comment(self):
        # Comment clasımızın blog içine related name verdik. vermeseydi 
        # altta comment olarak degilde comment_set diye getiririz.
        return self.comment.all()






class Comment(models.Model):
    blog = models.ForeignKey('Blog',null=True, max_length=100, on_delete=models.CASCADE, related_name='comment')
    isim = models.CharField(verbose_name='İsim', blank=True, null=True,max_length=50)
    soyisim = models.CharField(verbose_name='Soyisim', blank=True, null=True,max_length=50)
    email = models.EmailField(null=True,blank=False,verbose_name='e-mail', help_text='Bu alan boş bırakılamaz..')
    icerik = models.CharField(null=True,blank=False,max_length=1000,verbose_name='Yorum',help_text='Firinizi yazınız..')
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return '%s %s' % (self.email,self.blog)

    def get_screen_name(self):
        if self.isim:
            return '%s %s' % (self.isim,self.soyisim)
        return self.email
        