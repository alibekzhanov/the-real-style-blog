from django.shortcuts import render
from .models import Topics, Publication
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def home(request):
    publications = Publication.objects.all().order_by('-publish_date')
    paginator = Paginator(publications, 5)  # 5 публикаций на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        "topics": Topics.objects.all(),
        "page_obj": page_obj,
    }
    return render(request, 'base.html', context=context)


def page(request, page_name):
    page = Topics.objects.get(url=page_name)
    publications = Publication.objects.filter(page=page).order_by('-publish_date')
    paginator = Paginator(publications, 5)  # 5 публикаций на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        "page": page,
        "topics": Topics.objects.all(),
        "page_obj": page_obj,
    }
    return render(request, 'base.html', context=context)


# Представление для страницы выбора "selection_page"
def selection_page(request):
    return render(request, 'identity/selection_page.html')


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
    return render(request, 'identity/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'identity/register.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    if query:
        results = Publication.objects.filter(title__icontains(query))
    else:
        results = Publication.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})


def load_more(request):
    page_number = request.GET.get('page')
    publications = Publication.objects.all().order_by('-publish_date')
    paginator = Paginator(publications, 5)
    page_obj = paginator.get_page(page_number)
    
    publications_html = render_to_string('article.html', {'publications': page_obj.object_list})
    
    return JsonResponse({
        'publications_html': publications_html,
        'has_next': page_obj.has_next()
    })


def read_publication(request, publication_id):
    publication = Publication.objects.get(id=publication_id)
    context = {
        "publication": publication,
        "topics": Topics.objects.all()
    }
    return render(request, 'publication_detail/publication_detail.html', context=context)
