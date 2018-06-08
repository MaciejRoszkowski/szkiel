# from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Post

from django.http import Http404
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login



def index(request):
    latest_post_list = Post.objects.order_by('-Name')[:5]
    template = loader.get_template('mainapp/index.html')
    context = {
        'latest_post_list': latest_post_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, blog_id):

    return render(request, 'mainapp/detail.html', {'post': post})


def results(request, blog_id):
    response = "You're looking at name of blog %s."
    return HttpResponse(response % blog_id)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('index')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/registration.html', {'form': form})


def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")  # Redirect to a success page.
        else:
            return render(request, 'mainapp/login.html', {'message': "Invalid username or password."})
    return render(request, 'mainapp/login.html', {'login_form': form})
