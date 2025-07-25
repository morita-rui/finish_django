from django.shortcuts import render
from django.views import generic
from .models import Article
from django.urls import reverse_lazy

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
    
class CreateView(generic.CreateView):
    model = Article
    template_name = 'library/create.html'
    fields = '__all__'
    
class UpdateView(generic.UpdateView):
    model = Article
    template_name = 'library/create.html'
    fields = '__all__'

class DeleteView(generic.DeleteView):
    model = Article
    template_name = 'library/delete.html'
    success_url = reverse_lazy('library:index')

# Create your views here.
