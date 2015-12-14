from django.http import HttpResponse
from forms import AddForm

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            return HttpResponse("the url {0}".format(url))
    return HttpResponse("must use post")