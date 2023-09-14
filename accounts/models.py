from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name,user_type='customer', is_admin=False, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type,
            is_admin=is_admin
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, is_admin=False, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            user_type='super-admin',
            is_admin=is_admin
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
    ('super-admin', 'Super Admin'),
    ('staff', 'Staff'),
    ('customer', 'Customer'),)  
        
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,)
    name = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name',]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.user_type == 'super-admin' or self.user_type == 'staff'