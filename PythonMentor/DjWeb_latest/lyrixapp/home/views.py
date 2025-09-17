from django.shortcuts import render
from .models import Lyric

# Create your views here.
def lyrics_view(request, template_name='home.html'):
    lyric_list = Lyric.objects.all()
    return render(request, template_name, {'lyric_list': lyric_list})
