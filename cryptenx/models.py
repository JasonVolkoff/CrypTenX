from django.db import models
from calendar import timegm
# Create your models here.
class EtheriumData(models.Model):
    close_time = models.DateTimeField()
    open_price = models.DecimalField(max_digits=50, decimal_places=20)
    high_price = models.DecimalField(max_digits=50, decimal_places=20)
    low_price = models.DecimalField(max_digits=50, decimal_places=20)
    close_price = models.DecimalField(max_digits=50, decimal_places=20)
    volume = models.DecimalField(max_digits=50, decimal_places=20)
    quote_volume = models.DecimalField(max_digits=50, decimal_places=20)

    class Meta:
        ordering = ['close_time']

    def convert_to_unix(self):
        posix = str(timegm(self.close_time.timetuple()))
        return posix
    