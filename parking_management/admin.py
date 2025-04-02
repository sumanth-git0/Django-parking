from django.contrib import admin
from .models import parkuser, parkhistory, parkspace

# Register your models here.

admin.site.register(parkuser)
admin.site.register(parkhistory)
admin.site.register(parkspace)