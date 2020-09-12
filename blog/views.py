from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from .models import *
from .forms import*
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .decorators import *

mesajlar = []

def iletisim(request):
    form = IletisimForm(data = request.GET or None)

    # print(form.is_valid())

    if form.is_valid():

        isim = form.cleaned_data.get('isim')
        soyisim = form.cleaned_data.get('soyisim')
        email = form.cleaned_data.get('email')
        icerik = form.cleaned_data.get('icerik')
        
        # print(isim, soyisim, email, icerik)
        # bunu print etmemizin sebebi altta terminalde görüntüleyebilmek içindi

        data = {'isim':isim, 'soyisim':soyisim, 'email':email, 'icerik':icerik}
        
        mesajlar.append(data)

        return render(request, 'iletisim.html', context={'mesajlar':mesajlar, 'form':form})

    return render(request, 'iletisim.html', context={'form':form})



@login_required
def posts_list(request):
    
    posts = Blog.objects.all()
    page = request.GET.get('page',1)
    form = PostSorguForm(data=request.GET or None)

    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin', None)
        search = form.cleaned_data.get('search',None)
        if search:
            posts = posts.filter(
                Q(content__icontains=search) | Q(title__icontains=search) | Q(
                    kategoriler__isim__icontains=search)).distinct()

        if taslak_yayin and taslak_yayin != 'all':
            posts = posts.filter(yayin_taslak=taslak_yayin)
            # yayin_taslak modelden geliyor

    paginator = Paginator(posts,3)

    try:
        posts = paginator.page(page)

    except EmptyPage: # burda sayfa sayısından fazla girildiginde ne yapacagımızı yazalım.
        posts = paginator.page(paginator.num_pages) # num_page son sayfaya yönlendiriyoruz

    except PageNotAnInteger: # burda integer olmayan birşey girildiginde: 'qweqwe asd2312313123'
        posts = paginator.page(1) # burda 1. sayfaya gitsin

    context = {
        'post' : posts,
        'form' : form,
    }
    return render(request,'blog/post-list.html', context)





@login_required
def post_detail(request, slug):
    form = CommentForm()
    blog = get_object_or_404(Blog, slug=slug)

    return render(request, 'blog/post-detail.html', context={'blog':blog, 'form':form})





@login_required
@is_post
def add_comment(request, slug):
    blog = get_object_or_404(Blog,slug=slug)
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        # bu new_cooment sonrasi blog modeliimizin içindeki Comment clasının içindeki blog
        new_comment.save()
        messages.success(request,'Tebrikler yorumunuz başarıyla eklendi..')

        return HttpResponseRedirect(blog.get_absolute_url())




@login_required
def post_update(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    blog = get_object_or_404(Blog,slug=slug)
    form = BlogForm(instance=blog, data=request.POST or None, files=request.FILES or None)
    # files: 
    if form.is_valid():
        form.save()

        msg = "Tebrikler! <strong> %s </strong> İsimli Post'unuzu Güncellediniz." %(blog.title)
        messages.success(request, msg, extra_tags = 'info')
        # burda mavi renk olmasını istedigim için extra_tags = info yaptım
        return HttpResponseRedirect(blog.get_absolute_url())

    context = {
        'form' : form,
        'blog' : blog,
    }

    return render(request,'blog/post-update.html', context=context)





@login_required
def post_delete(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    blog = get_object_or_404(Blog,slug=slug)
    blog.delete()

    msg = "<strong> %s </strong> isimli Post'unuzu Sildiniz." %(blog.title)
    messages.success(request, msg, extra_tags = 'danger')

    return HttpResponseRedirect(reverse('post-list'))
# reverse, dememizin sebebi: detay sayfam yok sildik çünkü öyle bir alanım olmayacak
# post-list diyerek liste sayfamıza gönderelim. 





@login_required
def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    form = BlogForm()

    if request.method == "POST":
        form = BlogForm(data=request.POST, files=request.FILES)
        # files. ile media klasöründe yükleme işlemi gerçekleştirdim

        if form.is_valid():
            blog = form.save()

            msg = "Tebrikler! <strong> %s </strong> İsimli Post'unuz oluşturuldu." %(blog.title)
            messages.success(request, msg, extra_tags = 'success')

            return HttpResponseRedirect(blog.get_absolute_url())
            
    return render(request, 'blog/post-create.html', context={'form' : form})
