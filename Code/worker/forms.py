from django import forms
from .models import worker
from django.contrib.auth.forms import UserCreationForm , UsernameField,AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class workermodelform(forms.ModelForm):
    phonned = forms.BooleanField(required=False)
    search_query = forms.CharField(required=False,label='Search')

    class  Meta:
        model = worker
        fields =(
            'name','phone','email','addr','phonned','agent','search_query','comment',
        )

class customusercreationform(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username':UsernameField}

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search')

class CustomLoginForm(AuthenticationForm):
    # Add any custom form fields or override existing ones if needed
    # For example, you can add additional fields like "remember me" checkbox
    pass