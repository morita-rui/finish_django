from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Article, Loan
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.exceptions import PermissionDenied
from django import forms
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

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
    
class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    template_name = 'library/create.html'
    fields = ['title', 'isbn', 'author', 'publicationday', 'content']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['publicationday'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
        form.fields['title'].widget.attrs.update({'placeholder': '例: Python入門'})
        form.fields['isbn'].widget.attrs.update({'placeholder': '例: 123456789'})
        form.fields['author'].widget.attrs.update({'placeholder': '例: 山田太郎'})
        form.fields['content'].widget.attrs.update({'placeholder': '本の内容や説明を入力してください'})
        return form
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.username != 'admin':
            raise PermissionDenied('新規投稿は管理者のみ可能です。')
        return super(CreateView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
    
class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    template_name = 'library/create.html'
    fields = ['content']
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.username != 'admin':
            raise PermissionDenied('編集は管理者のみ可能です。')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    template_name = 'library/delete.html'
    success_url = reverse_lazy('library:index')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.username != 'admin':
            raise PermissionDenied('削除は管理者のみ可能です。')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

class BorrowView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        due_date = timezone.now().date() + timedelta(days=14)
        
        Loan.objects.create(
            article=article,
            user=request.user,
            borrow_date=timezone.now().date(),
            due_date=due_date
        )
        
        messages.success(request, f'「{article.title}」を貸出しました。返却期限は{due_date}です。')
        return redirect('library:detail', pk=pk)

class ReturnView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        
        current_loan = article.get_current_loan()
        
        if not current_loan:
            messages.error(request, 'この本は貸出されていません。')
            return redirect('library:detail', pk=pk)
        
        if current_loan.user != request.user and request.user.username != 'admin':
            messages.error(request, '返却権限がありません。')
            return redirect('library:detail', pk=pk)
        
        current_loan.return_date = timezone.now().date()
        current_loan.save()
        
        messages.success(request, f'「{article.title}」を返却しました。')
        return redirect('library:detail', pk=pk)

class MyLoansView(LoginRequiredMixin, generic.ListView):
    """ログインユーザーの借りている本一覧を表示"""
    model = Loan
    template_name = 'library/my_loans.html'
    context_object_name = 'loans'
    
    def get_queryset(self):
        return Loan.objects.filter(
            user=self.request.user,
            return_date__isnull=True
        ).select_related('article').order_by('due_date')


