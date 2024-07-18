from django.shortcuts import render
from .models import Topics, Publication
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    publications = Publication.objects.all().order_by('-publish_date')  # Получаем все публикации, сортируя их по дате публикации
    context = {
        "topics": Topics.objects.all(),
        "publications": publications,
    }
    return render(request, 'base.html', context=context)


def page(request, page_name):
    page = Topics.objects.get(url=page_name)
    context = {
        "publications": Publication.objects.filter(page=page),
        "topics": Topics.objects.all()
    }
    return render(request, 'base.html', context=context)


# представление для страницы выбора "selection_page"
def selection_page(request):
    return render(request, 'selection_page.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
