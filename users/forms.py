from django.forms import Form
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            style_data = {
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(style_data)


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['__all__']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            style_data = {
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(style_data)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = ('date_joined', 'last_login')
        fields = ['first_name',
                  'last_name',
                  'email',
                  'image']
        
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})
        }