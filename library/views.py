from django.shortcuts import render
from django.views import generic
from .models import Article

class IndexView(generic.ListView):
    model = Article
    template_name = 'library/index.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  
        if query:
            return queryset.filter(title__icontains=query) | queryset.filter(author__icontains=query)
        return queryset
    
class DetailView(generic.DetailView):
    model = Article
    template_name = 'library/detail.html'


# Create your views here.
