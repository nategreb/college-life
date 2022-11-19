from django.apps import apps
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.db import models as models
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from colleges.models import College


class CustomUserManager(UserManager): 
    
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email or not username or not password:
            raise ValueError('Users must have an email address, username, and password') 
    
        try:
            validate_email(email)
        except:            
            raise ValidationError('invalid email')
        
        email = self.normalize_email(email)
        
        college = College.all_colleges.get_college(email)
        
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)        
        user = self.model(
                    username=username, 
                    email=email, 
                    college=college,
                    **extra_fields
        )
        
        user.password = make_password(password)
        user.save(using=self._db)
        
        
        #add user to Groups with different college permissions
        #a staff is an admins and mods
        if extra_fields['is_staff']:
            user.groups.add(Group.objects.get_or_create(name='Admin')[0])            
        else: 
            user.groups.add(Group.objects.get_or_create(name='Regular User')[0])
        
        user.save(using=self._db)       
        return user

    def create_user(self, username, email, password=None, **extra_fields):        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_college_mod", False)       
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_college_mod", True)   

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)

    def create_admin(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_college_mod", True)
        extra_fields.setdefault("is_staff", True)   

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Admin must have is_staff=True.")
        return self._create_user(username, email, password, **extra_fields)
      
 
class User(AbstractUser):
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            )     
        ]
        db_table = 'auth_user'
        
    email           = models.EmailField(('email address'))
    college         = models.ForeignKey(
                        College, 
                        on_delete=models.CASCADE, 
                        blank=True, 
                        null=True                       
    )    
    is_college_mod  = models.BooleanField(default=False, blank=True)

    first_name      = None
    last_name       = None
    
    #default user manager
    objects         = CustomUserManager()
    
    #take an existing user and make them a college mod
    def make_college_mod(self):
        self.is_college_mod = True
        #remove from regular user group
        try:
            g = Group.objects.get(name='Regular User')
            self.groups.remove(g)
        except Group.DoesNotExist:
            print('regular user group doesn\t exist')        
            
        self.groups.add(Group.objects.get_or_create(name='Mods')[0])
        self.save()