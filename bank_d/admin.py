from django.contrib import admin

from .models import Banks, Branches
from django.contrib import admin

@admin.register(Banks)
class BanksAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name', )

@admin.register(Branches)
class BranchesAdmin(admin.ModelAdmin):
    list_display = (
        	'ifsc', 
        	'bank', 
        	'branch', 
        	'address', 
        	'city', 
        	'district', 
        	'state'
    )

    search_fields = ('ifsc', 'name', 'city')
    list_filter = ('bank',)