from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from .models import Author, Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = Author
        fields = [
            'name',
            'username',
            'email',
            
        ]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'website', 'gender', 'profile_picture', 'birthdate']


class AuthorAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Author
        fields = ('name', 'username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        author = super(AuthorAdminCreationForm, self).save(commit=False)
        author.set_password(self.cleaned_data["password1"])
        if commit:
            author.save()
        return author

class AuthorAdminChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Profile
        exclude = ('user', 'password')
    
    

