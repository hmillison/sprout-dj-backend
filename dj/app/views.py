from django.http import HttpResponse
from forms import AddForm

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the dj index.")

def add(request, list_id):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            return HttpResponse("the url {0} for list {1}".format(url, list_id))
    return HttpResponse("must use post")

def new_playlist(request):
    if request.method == 'POST':
        return HttpResponse("a new one")