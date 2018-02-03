from django.contrib import admin
from .models import WaterQualityRecord
# Register your models here.
class RecordAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'PH', 'DO', 'NH3N']
admin.site.register(WaterQualityRecord, RecordAdmin)