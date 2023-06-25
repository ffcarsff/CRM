from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect , reverse
from django.http import HttpResponse
from .models import worker,agent
from django.views.generic import TemplateView , ListView , DetailView ,CreateView , UpdateView , DeleteView
from .forms import workermodelform , customusercreationform , CustomLoginForm,SearchForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.db.models import Q

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    def get_success_url(self):
        return reverse('worker:worker-list')
   




# Create your views here.
class landingpageview(TemplateView):
    template_name = 'landing.html'
    
class signupview(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = customusercreationform
    def get_success_url(self):
        return reverse('login')

def landing_page(request):
    return render(request,'landing.html')

class workerlistview(LoginRequiredMixin,CreateView,ListView):
    template_name = 'worker/worker_list.html'
    context_object_name = 'worker'
    form_class = workermodelform
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
             queryset = worker.objects.filter(organisation = user.profile)
        else:
            queryset = worker.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset
    

def worker_list(request):
    #return HttpResponse('<h1>hello bitch</h1>')
    worker_data = worker.objects.all()
    context = {
        'worker':worker_data
    }
    return render(request,'worker/worker_list.html',context)

class workerdetailview(LoginRequiredMixin,DetailView):
    template_name = 'worker/worker_detail.html'
    context_object_name = 'worker'
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
             queryset = worker.objects.filter(organisation = user.profile)
        else:
            queryset = worker.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


def worker_detail(request , pk):
    worker_data = worker.objects.get(id=pk)
    context = {
        'worker':worker_data
    }
    return render(request,'worker/worker_detail.html',context)

class workercreateview(OrganiserAndLoginRequiredMixin,CreateView):
    template_name = 'worker/worker_create.html'
    form_class = workermodelform
  
  
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
             queryset = worker.objects.filter(organisation = user.profile)
        return queryset
    def get_success_url(self):
        return reverse('worker:worker-list')
   
    
def create_worker(request):
    form = workermodelform()
    if request.method == "POST":
        form = workermodelform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/worker')
    context ={
        "form":form
    }
    return render(request,'worker/worker_create.html',context)

class workerupdateview(OrganiserAndLoginRequiredMixin,UpdateView):
    template_name = 'worker/worker_update.html'
    
    form_class = workermodelform
    def get_success_url(self):
        return reverse('worker:worker-list')
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
             queryset = worker.objects.filter(organisation = user.profile)
        return queryset

def worker_update(request,pk):
    worker_data = worker.objects.get(id=pk)
    form = workermodelform(instance=worker_data)
    if request.method == "POST":
        form = workermodelform(request.POST,instance=worker_data)
        if form.is_valid():
            form.save()
            return redirect('/worker')
    context ={
        'worker':worker_data,
        "form":form
    }
    return render(request,'worker/worker_update.html',context)
class workerdeleteview(OrganiserAndLoginRequiredMixin,DeleteView):
    template_name = 'worker/worker_delete.html'
    def get_success_url(self):
        return reverse('worker:worker-list')
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
             queryset = worker.objects.filter(organisation = user.profile)
        return queryset



def worker_delete(request,pk):
    worker_data = worker.objects.get(id=pk)
    worker_data.delete()
    return redirect('/worker')



class YourMixin:
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = worker.objects.filter(organisation = user.profile)
        else:
            queryset = worker.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset
    def get_agents(self):
        agents_queryset = agent.objects.all()  # Query to retrieve agents
        return agents_queryset
        


        #return YourModel.objects.filter(condition=True)


class WorkerListView(YourMixin, View):
    template_name = 'worker/worker_list.html'

    def get(self, request):
        data_list = self.get_queryset()
        agents_list = self.get_agents()
        form = workermodelform()
        context = {
            'form': form,
            'worker': data_list,
            'agents': agents_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = workermodelform(request.POST)
        if form.is_valid():
            print("form is fking valid")
            form.save(commit=True)
            worker.objects.create(
                organisation = self.request.user.profile
        )
            return redirect('worker:worker-list')
        else:
            print(form.errors)
            

        data_list = self.get_queryset()
        context = {
            'form': form,
            'worker': data_list,
        }
        return render(request, self.template_name, context)
    



class SearchMixin(YourMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query)|Q(email__icontains=search_query)|Q(phone__icontains=search_query))  # Adjust the field name as per your model

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = workermodelform(self.request.GET)

        return context
    
class YourListView(SearchMixin, ListView):
    model = worker
    template_name = 'worker/worker_list.html'
    context_object_name = 'worker'
    