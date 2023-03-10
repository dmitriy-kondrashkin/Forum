from django.forms import Form
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
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
            'email': forms.EmailInput(attrs={'class':'form-control',
                                             'readonly': True,
                                             'disabled':True},
                                      )
        }


class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            style_data = {
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(style_data)


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs = {'class':'form-control'})  
    )

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())    