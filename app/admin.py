from django.contrib import admin
from .models import InvestModel, Stock , NewsHeadLines , UserCompany, ResponseModel

# Register your models here.
admin.site.register(NewsHeadLines)
admin.site.register(UserCompany)
# admin.site.register(ResponseModel)
class ResponseModelAdmin(admin.ModelAdmin):
    list_display = ('user','short_response')
    list_filter = ('user','response_Text')
    search_fields = ('user__username','response_Text')

    def short_response(self,obj):
        return (obj.response_Text[:30]+ '...') if len(obj.response_Text) > 30 else obj.response_Text
    short_response.short_description = "Response Preview"
class InvestModelAdmin(admin.ModelAdmin):
    list_display = ('user','company','stock_unit','base_price','total_price')
    list_filter = ('user',)
    search_fields = ('user__username','company__name')
    readonly_fields = ('total_price',)

    def total_price(self,obj):
        if obj.stock_unit is not None and obj.base_price is not None:
            return obj.stock_unit * obj.base_price
        return 0
    
    total_price.short_description = 'Total Price'

admin.site.register(InvestModel,InvestModelAdmin)
admin.site.register(ResponseModel,ResponseModelAdmin)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol","name")
    search_fields = ("symbol","name")