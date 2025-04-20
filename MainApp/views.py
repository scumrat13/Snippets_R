from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET': # создание пустой формы при GET запросе. Такой будет по лкм кнопки в хеддере
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == 'POST': # когда форма уже заполнена и лкм по кнопке создания
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False) # сохранение сниппета без добавления в базу
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snipp_list") # редикрект работает как GET на snippets/list
        return render(request, "pages/add_snippet.html", {'form': form})
    

def snippet_info(request, snipp_id:int):
    try:
        snippet = Snippet.objects.get(id=snipp_id)
    except ObjectDoesNotExist:
        return HttpResponse(f'<h2>Сниппета с id={snipp_id} не существует</h2>')
    else:
        context = {
            'pagename': 'Просмотр сниппета',
            'snippet': snippet,
            'type': 'view'
            }
        return render(request, "pages/snippet.html", context)


def snippets_page(request):
    if request.user.is_authenticated:
         snippets = Snippet.objects.filter(user=request.user)
    else:
        snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
               }
    return render(request, 'pages/view_snippets.html', context)


def snippet_delete(request, snipp_id:int):
    if request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snipp_id)
        snippet.delete()
        return redirect('snipp_list')


def snippet_edit(request, snipp_id:int):
    try:
        snippet = Snippet.objects.get(id=snipp_id)
    except ObjectDoesNotExist:
        return Http404
    
    if request.method == "GET": # Попадаем сюда по клику Редактировать сниппет
        context = {
        'pagename': 'Редактирование сниппета',
        'snippet': snippet,
        'type': 'edit',
        }
        return render(request, "pages/snippet.html", context)
    
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form['name']
        snippet.code = data_form['code']
        # snippet.creation_date = data_form['creation_date']
        snippet.save()
        return redirect('snipp_list')
    
def login(request):
	if request.method == 'POST':
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request, user)
		else:
			# обработать ошибку
			pass
	return redirect('home')

def logout(request):
	auth.logout(request)
	return redirect('home')
