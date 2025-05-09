from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Service, Campaign, Lead, Client, Contract

admin.site.site_header = "CRM Админка"
admin.site.site_title = "CRM Администрирование"
admin.site.index_title = "Управление CRM"

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'is_staff', 'is_active', 'groups')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {'fields': ('first_name', 'last_name',
                                            'email', 'role')}),
        ('Права доступа', {'fields': ('is_staff', 'is_active',
                                      'is_superuser',
                                      'groups', 'user_permissions')}),
        ('Дополнительно', {'fields': ('last_login',
                                      'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1',
                       'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'budget')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'campaign', 'is_converted')
    list_filter = ('is_converted', 'campaign')
    search_fields = ('name', 'email', 'phone')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('lead', 'joined_at')
    search_fields = ('lead__name',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'service', 'signed_date', 'valid_until', 'amount')
    list_filter = ('signed_date', 'valid_until', 'service')
    search_fields = ('title', 'client__lead__name', 'service__name')
