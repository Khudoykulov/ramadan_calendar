from django.contrib import admin
from .models import Region, DistrictTime, DefaultTime, Category, Surah
from datetime import datetime, date
from django.utils.timezone import timedelta

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', )


@admin.register(DistrictTime)
class DistrictTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'region__name', 'name', 'time_difference', 'saharlik_time', 'iftorlik_time')
    search_fields = ('region__name', 'name')
    def get_default_time(self):
        """ Oxirgi mavjud DefaultTime obyektini olish """
        return DefaultTime.objects.order_by('-date').first()

    def saharlik_time(self, obj):
        """ Saharlik vaqtini hisoblash """
        default_time = self.get_default_time()
        if default_time:
            saharlik_datetime = datetime.combine(date.today(), default_time.saharlik)
            new_time = saharlik_datetime + timedelta(minutes=obj.time_difference)
            return new_time.time().strftime("%H:%M")
        return "Noma'lum"

    def iftorlik_time(self, obj):
        """ Iftorlik vaqtini hisoblash """
        default_time = self.get_default_time()
        if default_time:
            iftorlik_datetime = datetime.combine(date.today(), default_time.iftorlik)
            new_time = iftorlik_datetime + timedelta(minutes=obj.time_difference)
            return new_time.time().strftime("%H:%M")
        return "Noma'lum"

    saharlik_time.short_description = "Saharlik"
    iftorlik_time.short_description = "Iftorlik"

@admin.register(DefaultTime)
class DefaultTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'saharlik', 'iftorlik')
    sortable_by = 'date'
    search_fields = ('date', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Surah)
class Surah(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'categories')
    filter_horizontal = ('categories', )