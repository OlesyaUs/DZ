from django.contrib import auth
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.forms import RegisterForm, LoginForm
from blog.models import *

# Create your views here.


def get_posts(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    data = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'posts.html', context=data)


def get_post(request, id):
    matList = ['blyat', 'her', 'niger']

    post = Post.objects.get(id=id)
    reviews = Review.objects.all().order_by('-updated').filter(post_id=id).exclude(text__in=matList)
    categories = Category.objects.all()

    data = {
        'post': post,
        'reviews': reviews,
        'categories': categories
    }

    if request.method == 'POST':
        author = request.POST.get('author')
        text = request.POST.get('text')
        Review.objects.create(author=author, text=text, post_id=id)

    return render(request, 'post.html', context=data)


def get_main(request):
    categories = Category.objects.all()

    data = {
        'categories': categories
    }
    return render(request, 'main.html', context=data)


def add_post(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        Post.objects.create(title=title, description=description, price=price)

    data = {
        'categories': categories,
    }

    return render(request, 'add_post.html', context=data)


def get_by_category(request, category_name):
    categories = Category.objects.all()
    category = Category.objects.filter(name=category_name)
    posts = Post.objects.filter(category__in=category)

    data = {
        'posts': posts,
        'category': category_name,
        'categories': categories
    }
    return render(request, 'postsByCategory.html', context=data)


def add_category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('category')
        category = Category.objects.filter(name=name)
        if not category:
            Category.objects.create(name=name)
        else:
            return HttpResponse("NO")

    data = {
        'categories': categories
    }

    return render(request, 'add_category.html', context=data)


def register(request):
    categories = Category.objects.all()
    if request.method =='POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return render(request, 'register.html', context={
                'form': RegisterForm
            })

    data = {
        'categories': categories,
        'form': RegisterForm
    }

    return render(request, 'register.html', context=data)


def login(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
            return redirect('/')

    data = {
        'categories': categories,
        'form': LoginForm
    }

    return render(request, 'login.html', context=data)