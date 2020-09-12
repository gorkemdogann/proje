from django.http import HttpResponseBadRequest
from django.shortcuts import reverse, HttpResponseRedirect, redirect



def is_post(func):
    def wrap(request, *args, **kwargs):
        
        if request.method  == 'GET':
            # return HttpResponse('HATA MSJI')
            return HttpResponseBadRequest()
            # burda get işlemi varsa hatalı dönder.

        return func(request, *args, **kwargs)
    
    return wrap



def anonymous_required(func):

    def wrap(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('post-list'))
            # return redirect('post-list')

        func(request, *args, **kwargs)
    
    return wrap

