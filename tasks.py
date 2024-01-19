from datetime import datetime, timedelta
from time import timezone
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail

from course.models import Course
from config import settings
from users.models import User
# from course.signals import set_previous_modified_at
from lesson.models import Lesson
from subscription.models import Subscription

@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(pk=course_id)  # Метод get() уже возвращает один объект, поэтому не нужно использовать filter().get()
    if (course.modified_at.replace(tzinfo=None) - timedelta(hours=4)) < (course.previous_modified_at.replace(tzinfo=None)):
        # Преобразуем modified_at в offset-naive datetime
        subscribers = Subscription.objects.get(course=course, is_active=True)  # Используем метод get() вместо filter().get()
        send_mail(
            'Обновление курса',
            f'Курс "{course.title}" был обновлен. Посетите страницу курса для получения более подробной информации.',
            settings.EMAIL_HOST_USER,
            [subscribers.user.email]
        )


@shared_task
def send_lesson_update_notification(lesson_id):
    lesson = Lesson.objects.filter(pk=lesson_id).get()
    course_id = lesson.course.id
    course = Course.objects.filter(pk=course_id).get()
    subscribers = Subscription.objects.filter(course=course, is_active=True).get()
    send_mail(
        'Обновление урока',
        f'Урок "{lesson.title}" был обновлен. Посетите страницу курса для получения более подробной информации.',
                 settings.EMAIL_HOST_USER,
        [subscribers.user.email]
    )

@shared_task
def user_unactive():
    users = User.objects.all()
    one_month_ago = timezone.now() - timedelta(days=30)



    for user in users:
        if user.last_login < one_month_ago:  # Проверяем, прошло ли более месяца с момента последнего входа
            user.is_active = False  # Устанавливаем флаг is_active в False
            user.save()  # Сохраняем изменения

