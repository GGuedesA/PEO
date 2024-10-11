from django.contrib.auth.base_user import BaseUserManager
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

class StudentManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        
        try:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
        except IntegrityError:
            raise ValueError(_("A user with this email already exists"))
        return user
    