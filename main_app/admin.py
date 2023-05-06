from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustEnq,EnqDtl,Review

class CAdmin(admin.ModelAdmin):
    list_display = ("id","name","phone","email","query","date_created")

class RAdmin(admin.ModelAdmin):
    list_display = ("id","enqno","rspno","satisfied","date_created")

class EAdmin(admin.ModelAdmin):
    list_display = ("id","qry_response","date_created")

admin.site.register(CustEnq,CAdmin)
admin.site.register(Review,RAdmin)
admin.site.register(EnqDtl,EAdmin)


