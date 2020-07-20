from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AuthorAdminCreationForm, AuthorAdminChangeForm
from .models import Author, Profile


class AuthorAdmin(BaseUserAdmin):
    form = AuthorAdminChangeForm
    add_form = AuthorAdminCreationForm

    list_display = ('name', 'username', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'following')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'username', 'email', 'password1', 'password2')
            }
         ),
    )
    search_fields = ('email',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Author, AuthorAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
