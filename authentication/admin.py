from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from authentication.models import User, FriendRequest


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "first_name", "is_staff",)
    search_fields = ("first_name", "email")
    ordering = ("email",)
    readonly_fields = ["created_at", "updated_at", ]


admin.site.register(User, UserAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    # List of fields to display in the list view
    list_display = ('id', 'sender', 'receiver', 'status',)

admin.site.register(FriendRequest, FriendRequestAdmin)