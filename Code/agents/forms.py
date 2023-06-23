from django import forms
from worker.models import agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
user = get_user_model()

class AgentModelForm(UserCreationForm):
    Task_completion = forms.BooleanField()
    class Meta:
        model = user
        fields = ('username','first_name','last_name','email',)

    class Af:
        model = agent
        fields = ('Task_completion')
  