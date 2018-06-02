# from django.shortcuts import render


from django.http import HttpResponse
from django.template import loader
from .models import Blog, Post
from django.shortcuts import render
from django.http import Http404


def index(request):
    latest_blog_list = Blog.objects.order_by('-Name')[:5]
    template = loader.get_template('mainapp/index.html')
    context = {
        'latest_blog_list': latest_blog_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
        post = Post.objects.filter(blog=blog_id)
    except Blog.DoesNotExist:
        raise Http404("nie ma bloga ")
    return render(request, 'mainapp/detail.html', {'blog': blog, 'post': post})


def results(request, blog_id):
    response = "You're looking at name of blog %s."
    return HttpResponse(response % blog_id)

