from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile
from django.contrib.auth.models import PermissionsMixin, Permission
from .forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm

class UserAdmin(UserAdmin):
	form = UserUpdateForm
	add_form = RegistrationForm
	list_display = ('email','username', 'full_name', 'date_joined', 'last_login', 'is_author', 'is_staff', 'is_admin')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login', 'password')

	model = User

	list_filter = ()
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('is_author', 'is_staff', 'is_admin', 'is_active', 'groups', 'user_permissions')}),('Important dates', {'fields': ('last_login', 'date_joined')}),
		)

	search_fields = ('email',)
	ordering = ('email',)


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bio')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

