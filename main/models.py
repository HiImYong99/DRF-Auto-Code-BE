from django.db import models
from accounts.models import User
# Create your models here.

language_select = (
    ('C', 'C'),
    ('C++', 'C++'),
    ('C#', 'C#'),
    ('Go', 'Go'),
    ('Java', 'Java'),
    ('JavaScript', 'JavaScript'),
    ('Kotlin', 'Kotlin'),
    ('Python3', 'Python3'),
)

purpose_select = (
    ('기능구현', '기능구현'),
    ('리팩토링', '리팩토링')
)


class UserInput(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    language = models.CharField(
        max_length=20, choices=language_select
    )
    purpose = models.CharField(
        max_length=5, choices=purpose_select
    )
    detail = models.TextField()

    def __str__(self):
        return f'{self.user}의 {self.language} {self.purpose}'


class AIOutput(models.Model):
    userinput = models.ForeignKey(
        'main.UserInput', on_delete=models.CASCADE
    )
    answer = models.TextField()

    def __str__(self):
        return f'{self.userinput}에 대한 응답'
