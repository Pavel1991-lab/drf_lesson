from datetime import timedelta

from django.db.models.signals import pre_save
from django.dispatch import receiver
from course.models import Course
from django.utils import timezone


@receiver(pre_save, sender=Course)
def set_previous_modified_at(sender, instance, **kwargs):
    if instance.pk:  # Если у текущего экземпляра уже есть первичный ключ
        previous_instance = Course.objects.get(pk=instance.pk)  # Получаем предыдущий экземпляр из базы данных
        instance.previous_modified_at = previous_instance.previous_modified_at  # Устанавливаем previous_modified_at текущего экземпляра
    else:  # Если у текущего экземпляра нет первичного ключа
        instance.previous_modified_at = None  # Устанавливаем previous_modified_at в None



