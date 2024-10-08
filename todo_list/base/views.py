from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , LogoutView
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class CustomLogin(LoginView):
    template_name = 'base/Login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('base')

class RegisterPage(FormView):
    template_name = 'base/Register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('base')
    redirect_authenticated_user = True
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base')
        return super(RegisterPage, self).get(*args, **kwargs)
        


class TakeList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    @csrf_exempt
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(user = self.request.user).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains = search_input)
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    pk_url_kwarg = 'id'

class CreateTask(LoginRequiredMixin,CreateView):
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base')
    template_name = 'base/create-task.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

class EditTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'base/update_task.html'
    success_url = reverse_lazy('base')

class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('base')
    template_name = 'base/delete_task.html'