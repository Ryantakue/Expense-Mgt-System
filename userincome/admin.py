from django.contrib import admin
from .models import UserIncome, Source
# Register your models here.

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date',)
    search_fields = ('description', 'category', 'date',)

    list_per_page = 5


admin.site.register(UserIncome,IncomeAdmin)
admin.site.register(Source)