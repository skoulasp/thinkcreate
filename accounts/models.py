from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from thinkcreate.storage import OverwriteStorage

# Create your models here.

class MyUserManager(BaseUserManager):
	def create_user(self, email, username, full_name, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not full_name:
			raise ValueError("Users must have a full name")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			full_name=full_name,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, email=None, password=None, **extra_fields):
		user = self.create_user(self, email, username, full_name, password=None)
		user.is_staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, full_name, password, **extra_fields):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			full_name=full_name,
		)
		user.is_author = True
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	full_name = models.CharField(verbose_name="full name", max_length=60, null=True, blank=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_author = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'full_name']

	objects = MyUserManager()

	def __str__(self):
		if self.full_name != '':
			return self.full_name
		return self.username

	def has_module_perms(self, app_label):
		return True


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(null=True, blank=True)
	image = models.ImageField(storage=OverwriteStorage(), default='uploads/profile_images/default.png', upload_to='uploads/profile_images', null=True, blank=True)
	def getImage(self):
		if not self.image:
			return default_path or default_image_object

	def __str__(self):
		return f'{self.user.username} Profile'	


