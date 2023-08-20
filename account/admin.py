from django.contrib import admin
from account.models import User, InviteCode
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id")


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "id")
    raw_id_fields = ("user", "users_activate_invite")
    list_select_related = ("user",)
    readonly_fields = ("code",)