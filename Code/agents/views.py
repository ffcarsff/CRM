from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect , reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView , ListView , DetailView ,CreateView , UpdateView , DeleteView

from worker.models import agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q
# Create your views here.

class AgentListView(OrganiserAndLoginRequiredMixin,generic.ListView):
    template_name = 'agents/agents_list.html'

    def queryset(self):
        organisation = self.request.user.profile
        return agent.objects.filter(organisation= organisation)
    
class AgentCreatView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name = 'agents/agents_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents_list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_aagent = True
        user.is_organiser = False
        user.save()
        agent.objects.create(
            user=user,
           
            organisation = self.request.user.profile
        )
        
        return super(AgentCreatView, self).form_valid(form)
    
class AgentDetailView(OrganiserAndLoginRequiredMixin,generic.DetailView):
    template_name = 'agents/agents_detail.html'
    context_object_name = 'agent'
    def get_queryset(self):
        
        organisation = self.request.user.profile
        return agent.objects.filter(organisation= organisation)
    
class AgentUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'agents/agents_update.html'
    form_class = AgentModelForm
    #context_object_name = 'agent'
    def get_queryset(self):
        organisation = self.request.user.profile
        return agent.objects.filter(organisation= organisation)
    def get_success_url(self):
        return reverse('agents:agents_list')
class AgentDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name = 'agents/agents_delete.html'
    
    context_object_name = 'agent'
    def get_success_url(self):
        return reverse('agents:agents_list')
    def get_queryset(self):
        organisation = self.request.user.profile
        return agent.objects.filter(organisation= organisation)
    
class AgentListViewU(OrganiserAndLoginRequiredMixin,generic.ListView):
    template_name = 'agents/agents_list.html'
    
    def queryset(self):
        organisation = self.request.user.profile
        return agent.objects.filter(organisation= organisation)


    def get(self, request):
        data_list = self.get_queryset()
        form = AgentModelForm()
        context = {
            'form': form,
            'worker': data_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AgentModelForm(request.POST)
        if form.is_valid():
            print("form is fking valid")
            form.save(commit=True)
            return redirect('agents:agents-list')
        else:
            print(form.errors)
            

        data_list = self.get_queryset()
        context = {
            'form': form,
            'worker': data_list,
        }
        return render(request, self.template_name, context)
    


class UserView(OrganiserAndLoginRequiredMixin,TemplateView):
    template_name = 'agents/agents_list.html'

  


    def get(self, request):
        organisation = self.request.user.profile
        data_list = agent.objects.filter(organisation= organisation)
        form = AgentModelForm()
        context = {
            'form': form,
            'agent': data_list,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AgentModelForm(request.POST)
        if form.is_valid():
            # Process form data and create the user
             user = form.save(commit=False)
             user.is_aagent = True
             user.is_organiser = False
             user.save()
             agent.objects.create(
                 user=user,
                 organisation = self.request.user.profile
                 )
            # Perform user creation logic here


        return redirect('agents:agents_list')
    
class SearchMixin(OrganiserAndLoginRequiredMixin):
    def get_queryset(self):
        organisation = self.request.user.profile
        queryset = agent.objects.filter(organisation= organisation)
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(Q(user_id__username__icontains=search_query)|Q(user_id__email__icontains=search_query))
  # Adjust the field name as per your model

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AgentModelForm(self.request.GET)

        return context
    
class YourListView(SearchMixin, ListView):
    model = agent
    template_name = 'agents/agents_list.html'
    context_object_name = 'agent'
    