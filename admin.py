from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'blood_group',
        'age',
        'gender',
        'city',
        'phone',
        'availability',
        'created_at'
    )
    list_filter = ('blood_group', 'availability', 'city', 'gender')
    search_fields = ('full_name', 'city', 'phone', 'email', 'blood_group')
    list_editable = ('availability',)
    ordering = ('-created_at',)
    list_per_page = 20
