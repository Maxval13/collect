from django.db import models
from django.conf import settings
import uuid
import os


def image_file_path(instande, filename):
    """ Cоздать путь к файлу для нового изображения"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('upload/collect/', filename)


class Attendee(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    image = models.ImageField(null=True, upload_to=image_file_path, verbose_name='Аватарка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Account(models.Model):
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='Баланс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id} of {self.user.username}'


class Action(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='сумма пополнения')
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='actions',
                                verbose_name='счет зачисления')

    def __str__(self):
        return f'Account number {self.account.id} ' + \
            f'was changed on {str(self.amount)}'


class Payment(models.Model):
    full_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ФИО пользователя')
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма пожертвования')
    datetime_pay = models.DateTimeField(auto_now_add=True)


class Reason(models.Model):
    name = models.CharField(max_length=50, verbose_name='Повод сбора средств')

    def __str__(self):
        return self.name


class Collect(models.Model):
    author_collection = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор сбора')
    name_collection = models.CharField(max_length=30, verbose_name='Название')
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, verbose_name='Повод')
    content = models.TextField(verbose_name='Описание')
    amount_full = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма для сбора')
    amount_now = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма собранных средств')
    count = models.IntegerField()
    image = models.ImageField(null=True, upload_to=image_file_path)
    deadline_date = models.DateTimeField()
    tape = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='Лента сбора')
