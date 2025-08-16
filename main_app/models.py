from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from datetime import date


class UserManager(BaseUserManager):
    def create_user(self, name, email, password, chief=None):
        if not name or not email or not password:
            raise ValueError('Some required fields are empty')
        user = self.model(email=self.normalize_email(email), name=name, chief=chief)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Qualification(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    chief = models.ForeignKey('self',
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='subordinates')
    qualifications = models.ManyToManyField(Qualification)
    languages = models.ManyToManyField(Language)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return f'{self.name}'

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    @staticmethod
    def has_module_perms(self, app_label):
        return True


@receiver(pre_delete, sender=User)
def update_user_on_chief_delete(sender, instance, **kwargs):
    subs = User.objects.filter(chief_id=instance)
    new_chief = instance.chief_id
    subs.update(chief_id=new_chief)


class Task(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateField()
    report_required = models.BooleanField(default=False)
    qualifications_required = models.ManyToManyField(Qualification)
    language_required = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class ArchiveTaskManager(models.Manager):
    def create_from_task(self, task):
        return self.create(
            name=task.name,
            deadline=task.deadline,
            report_required=task.report_required,
            performer=task.performer,
            completion_date=date.today()
        )

    def from_task(self, task):
        return self.model(
            name=task.name,
            deadline=task.deadline,
            report_required=task.report_required,
            performer=task.performer,
            completion_date=date.today()
        )


class ArchiveTask(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateField()
    report_required = models.BooleanField(default=False)
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completion_date = models.DateField()

    objects = ArchiveTaskManager()
