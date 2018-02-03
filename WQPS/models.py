from django.db import models

# Create your models here.
class WaterQualityRecord(models.Model):
    station = models.IntegerField(verbose_name=u'监测站编号', blank=False, null=False,default=0)
    year = models.IntegerField(verbose_name=u'年份', blank=False, null=False)
    month = models.IntegerField(verbose_name=u'月份', blank=False, null=False)
    PH = models.DecimalField(verbose_name=u'PH', max_digits=6, decimal_places=3, blank=False, null=False)
    DO = models.DecimalField(verbose_name=u'溶解氧', max_digits=6, decimal_places=3, blank=False, null=False)
    NH3N = models.DecimalField(verbose_name=u'氨氮', max_digits=6, decimal_places=3, blank=False, null=False)
    class Meta:
        ordering = ['station','year','month']
