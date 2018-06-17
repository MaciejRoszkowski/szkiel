# from django.shortcuts import render

import json
import urllib
from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


from .models import Post, Comment
from django.http import Http404
from .forms import SignUpForm, LoginForm, NewPostForm, CommentForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def index(request):
    latest_post_list = Post.objects.order_by('-postDate')
    template = loader.get_template('mainapp/index.html')
    context = {
        'latest_post_list': latest_post_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, post_id):
    post = Post.objects.filter(pk=post_id)
    comment = Comment.objects.filter(post_id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm()

    return render(request, 'mainapp/detail.html', {'post': post, 'comment': comment, 'form': form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/registration.html', {'form': form})


def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.login(request)
            if user:
                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                ''' End reCAPTCHA validation '''
                if result['success']:
                    login(request, user)
                    return HttpResponseRedirect("/")  # Redirect to a success page.
        else:
            return render(request, 'mainapp/login.html', {'message': "Invalid username or password."})
    return render(request, 'mainapp/login.html', {'login_form': form})


def newPost(request):
    if request.POST:
        form = NewPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.author = request.user
            newPost.postDate = datetime.datetime.now()
            newPost.save()
            return HttpResponseRedirect("/")
    else:
        form = NewPostForm()
    return render(request, 'mainapp/newPost.html', {'form': form})


def generatePdf(request, post_id):
    filename = "%s.pdf" % str(Post.objects.get(id=post_id).id)
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    Story = [Spacer(5, 2)]
    Story.append(Paragraph(Post.objects.get(id=post_id).title, styles["title"]))
    Story.append(Spacer(1, 0.2 * inch))
    Story.append(Paragraph("Posted by " + Post.objects.get(id=post_id).author.username
                           + " on " + Post.objects.get(id=post_id).postDate.strftime("%Y-%m-%d"), styles["Normal"]))
    Story.append(Spacer(1, 0.2 * inch))
    if Post.objects.get(id=post_id).postImage:
        im = Image(Post.objects.get(id=post_id).postImage, 3 * inch, 3 * inch)
        Story.append(im)
    Story.append(Paragraph(Post.objects.get(id=post_id).short_description, styles["Normal"]))
    Story.append(Spacer(1, 0.2 * inch))
    Story.append(Paragraph(Post.objects.get(id=post_id).text, styles["Normal"]))
    Story.append(Spacer(1, 0.2 * inch))
    doc.build(Story)
    fs = FileSystemStorage("")
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="%s"' % filename
        return response
    return response

def search(request):
    query = request.GET['search']
    posts = []
    postsText = Post.objects.filter( text__icontains = query)
    postsShortDescription = Post.objects.filter( short_description__icontains=query)
    postsTitle = Post.objects.filter( title__icontains=query)
    postsRepeats = chain(postsText,postsTitle, postsShortDescription)
    [posts.append(item) for item in postsRepeats if item not in posts]
    return HttpResponse(render(request, 'mainapp/search.html', {'query': query, 'posts': posts}))