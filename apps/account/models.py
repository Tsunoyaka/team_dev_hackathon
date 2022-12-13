from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('User must have username')
        if not email:
            raise ValueError('User must have email')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    PATH_TO_USERPICK = 'satanael2.png'

    username = models.CharField('Username', max_length=50)
    email = models.EmailField('Email', max_length=255, primary_key=True)
    image = models.ImageField(upload_to='user_images', default=PATH_TO_USERPICK, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
