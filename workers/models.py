from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Worker(models.Model):
    user = models.OneToOneField(User, related_name="worker", unique=True, blank=True, null=True, default=None,
                                on_delete=models.CASCADE)

    first_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    surname = models.CharField(max_length=128, blank=True, null=True, default=None)

    email = models.EmailField(blank=True, null=True, default=None)

    speciality = models.CharField(max_length=128, blank=True, null=True, default=None)
    experience = models.DecimalField(max_digits=30, decimal_places=0, blank=True, null=True, default=None)
    money = models.DecimalField(max_digits=10000, decimal_places=2, blank=True, null=True, default=None)

    def __str__(self):
        return "Работник %s" % self.id

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

@receiver (post_save, sender=User)
def user_created(sender, instance=None, created=False, **kwargs):
    if created:
        Worker.objects.create(user=instance, )

