from django.contrib import admin
from .models.profile import Profile
from .models.roles import Role


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'loyalty_status', 'tier']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]

