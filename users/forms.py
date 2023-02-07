from django.forms import Form
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['__all__']



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = ('date_joined', 'last_login')
        fields = ['first_name',
                  'last_name',
                  'email']
        
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})
        }