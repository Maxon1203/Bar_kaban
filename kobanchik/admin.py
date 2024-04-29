from django.contrib import admin

# Register your models here.
from  .models import *

@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass