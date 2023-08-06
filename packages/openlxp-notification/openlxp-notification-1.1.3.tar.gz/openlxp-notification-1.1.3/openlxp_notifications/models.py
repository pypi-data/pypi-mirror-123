from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from model_utils.models import TimeStampedModel

from openlxp_notifications.management.utils.notification import \
    email_verification


class ReceiverEmailConfiguration(TimeStampedModel):
    """Model for Receiver Email Configuration """

    email_address = models.EmailField(
        max_length=254,
        help_text='Enter email personas addresses to send log data',
        unique=True)

    def get_absolute_url(self):
        """ URL for displaying individual model records."""
        return reverse('Configuration-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

    def save(self, *args, **kwargs):
        email_verification(self.email_address)
        return super(ReceiverEmailConfiguration, self).save(*args, **kwargs)


class SenderEmailConfiguration(TimeStampedModel):
    """Model for Sender Email Configuration """

    sender_email_address = models.EmailField(
        max_length=254,
        help_text='Enter sender email address to send log data from')

    def save(self, *args, **kwargs):
        if not self.pk and SenderEmailConfiguration.objects.exists():
            raise ValidationError('There is can be only one '
                                  'SenderEmailConfiguration instance')
        return super(SenderEmailConfiguration, self).save(*args, **kwargs)


class EmailConfiguration(TimeStampedModel):
    """Model for Email Configuration """

    SUBJECT = models.CharField(max_length=200, null=True)

    HTML_File = models.FileField(help_text='Upload the html file')

    LOG_PATH = models.CharField(max_length=200, null=True)

    def get_absolute_url(self):
        """ URL for displaying individual model records."""
        return reverse('Configuration-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

    def save(self, *args, **kwargs):
        return super(EmailConfiguration, self).save(*args, **kwargs)
