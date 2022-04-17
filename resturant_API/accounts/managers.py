from django.contrib.auth.models import BaseUserManager, Group


class UserManager(BaseUserManager):
   
    # use_in_migrations = True
    admin_role = 1

    def _create_user(self, employee_number, password, **extra_fields):
        ''' Create and save a user with the given employee_number and password '''

        employee_number = self.model.normalize_username(employee_number)
        user = self.model(employee_number=employee_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # if user's role is 1 then, the user will be added to admins group
        admins_group  = Group.objects.get(name='Admins')
        if extra_fields.get('role') == self.admin_role:
            admins_group.user_set.add(user)
            admins_group.save()

        return user


    def create_superuser(self, employee_number, password, **extra_fields):
        '''Create and save a SuperUser with the given email and password.'''

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have an Admin role')

        return self._create_user(employee_number, password, **extra_fields)
