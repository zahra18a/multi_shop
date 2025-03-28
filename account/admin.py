from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from account.models import User, Otp, Address


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", 'full_name', "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("اطلاعات شخصی", {"fields": ["full_name"]}),
        ("دسترسی ها", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone"]
    ordering = ["phone"]
    filter_horizontal = []




admin.site.register(User, UserAdmin)
admin.site.register(Otp)
admin.site.register(Address)
admin.site.unregister(Group)
