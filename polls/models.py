import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from datetime import datetime, timedelta
import pytz


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=50, help_text="Напишите ФИО")
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=254)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, upload_to="images/profile")

    USERNAME_FIELD = 'username'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # Список имён полей для Superuser

    objects = UserManager()

    def __str__(self):
        return self.username


class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now())
    ex_date = models.DateTimeField(default=datetime.now() + timedelta(days=1),
                                   verbose_name='Время жизни',
                                   null=False)
    votes = models.IntegerField(default=0)
    img = models.ImageField(null=True, default='default.jpg', upload_to="images/question")
    description = models.TextField(max_length=600, null=True)
    description2 = models.TextField(max_length=600, null=True)
    voted_by = models.ManyToManyField(User, verbose_name='проголосовавшие', blank=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        all_votes = Choice.objects.all()
        votes_count = 0
        for obj in all_votes:
            votes_count += obj.votes
        if self.votes != 0:
            return round((self.votes / votes_count) * 100)
        else:
            return 0

    def __str__(self):
        return self.choice_text
