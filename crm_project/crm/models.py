from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('operator', 'Оператор'),
        ('marketer', 'Маркетолог'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='marketer')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role.capitalize())
            self.groups.set([group])

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # новое поле

    def __str__(self):
        return str(self.name)

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Услуга
    promotion_channel = models.CharField(max_length=255)  # Канал продвижения


    def __str__(self):
        return str(self.name)

class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)
    is_converted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Client(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.lead)


class Contract(models.Model):
    title = models.CharField(max_length=255, default="Новый контракт")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    document = models.FileField(upload_to='contracts/')
    signed_date = models.DateField()
    valid_until = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.title)
