from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from blog import models
# Create your views here.
def index(request):
    articles = models.Artic.objects.all()
    return render(request, 'blog/index.html', {'articles': articles})

#def yuanxin(request):
#    wyx = models.Artic.objects.get(pk=2)
#    return render(request, 'blog/index.html', {'wyx': wyx})

def article_page(request, article_id):
    article = models.Artic.objects.get(pk=article_id)
    return render(request, 'blog/article_page.html', {'article': article})

def edit_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'blog/edit_page.html')
    article = models.Artic.objects.get(pk=article_id)
    return render(request, 'blog/edit_page.html', {'article': article})

def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    article_id = request.POST.get('article_id', '0')
    if str(article_id) == '0':
        models.Artic.objects.create(title=title, content=content)
        #articles = models.Artic.objects.all()
        #return render(request, 'blog/index.html', {'articles': articles})
        return HttpResponseRedirect('/blog/index/')
    article = models.Artic.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    return render(request, 'blog/article_page.html', {'article': article})

def ok(request):
    return HttpResponse('ok')