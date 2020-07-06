from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Author

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Author
        fields = ('name', 'username', 'email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Author.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = Author.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    

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

class AuthorAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Author
        fields = ('username', 'email', 'password', 'active', 'admin')
    
    def clean_password(self):
        return self.initial["password"]