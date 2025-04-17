from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)

def snippet_page(request, snipp_id:int):
    try:
        snippet = Snippet.objects.get(id=snipp_id)
    except ObjectDoesNotExist:
        return HttpResponse(f'<h2>Сниппета с id={snipp_id} не существует</h2>')
    else:
        context = {
            'pagename': 'Просмотр сниппета',
            'snippet': snippet
            }
        return render(request, "pages/snippet.html", context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
               }
    return render(request, 'pages/view_snippets.html', context)
