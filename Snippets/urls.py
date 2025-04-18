from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="snipp_add"),
    path('snippets/list', views.snippets_page, name="snipp_list"),
    path('snippets/<int:snipp_id>/', views.snippet_page, name='snipp_info'),
    path('snippets/<int:snipp_id>/delete', views.snippet_delete, name='snipp_delete'),
    path('snippets/<int:snipp_id>/edit', views.snippet_edit, name='snipp_edit')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
