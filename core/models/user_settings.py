from django.db import models

__author__ = 'Ashraful'


class Settings(models.Model):
    email_notification = models.BooleanField(default=False, verbose_name="Email Notification")
    web_notification = models.BooleanField(default=False, verbose_name="Web Notification")

    def __str__(self):
        return "{0}".format("Settings")  # TODO will update this later
