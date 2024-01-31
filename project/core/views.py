from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .filters import CommentFilter

class ArticleList(ListView):
    model = Article

    ordering_by = '-id'
    
    template_name = 'articlelist.html'

    context_object_name = 'articlelist'
    paginate_by=30

class ArticleDetail(FormMixin, DetailView):

    model = Article
    form_class = CommentForm
    template_name = 'article.html'
    context_object_name = 'articledetail'


    def get_success_url(self) -> str:
        return reverse_lazy('detail', kwargs={'pk':self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = form.save(commit=False)
        if form.is_valid():
            email = self.get_object().author.email
            subject = f'У вашей статьи новый отклик!'
            text_content = (
                f'пользователь {self.request.user} оставил отклик под вашей статьёй\n'
                f'С названием {self.object.text}'
            )
            html_content = (
                f'пользователь {self.request.user} оставил отклик под вашей статьёй<br>'
                f'С названием {self.object.text}'
            )
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = 'это тест'
        return context

class AddArticle(LoginRequiredMixin, CreateView):
    model = Article

    form_class = ArticleForm

    template_name = 'addarticle.html'

    success_url = reverse_lazy('list')

    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
class ArticleChange(LoginRequiredMixin, UpdateView):

    model = Article

    form_class = ArticleForm

    template_name = 'checkarticle.html'

    # def get_form_kwargs(self):
    #     kwargs =  super().get_form_kwargs()
    #     print(kwargs)
    #     return kwargs    
    
class ArticleDelete(LoginRequiredMixin, DeleteView):
    
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('list')

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        self.object = self.get_object()
        print(self.request.user.email)
        print(self.get_object().author.username)
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class CommentList(LoginRequiredMixin, ListView):

    model = Comment
    ordering_by='-id'
    template_name = 'comments.html'
    context_object_name = 'commentlist'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.id
        context['filterset'] = self.filterset

        return context

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect('/articles/comments/'+ str(request.user.id))

def reply_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    email = comment.author.email
    subject = f'ваш отклик понравился автору!'
    text_content = (
        f'автор статьи {comment.article} подтвердил ваш отклик\n'
        f'С содержанием {comment.text}'
    )
    html_content = (
        f'пользователь {comment.article} подтвердил ваш отклик<br>'
        f'С содержанием {comment.text}'
    )
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    comment.replied = not comment.replied
    comment.save()
    return redirect('/articles/comments/'+ str(request.user.id))

