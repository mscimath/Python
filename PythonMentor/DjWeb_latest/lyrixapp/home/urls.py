from django.urls import path
from .views import lyrics_view

urlpatterns = [
    path('', lyrics_view,{'template_name': 'home.html'}, name='home' ),
    path('home/', lyrics_view, {'template_name': 'home.html'}, name='home'),
    path('lyrics/', lyrics_view, {'template_name': 'lyric_list.html'}, name='lyric_list'),
]
