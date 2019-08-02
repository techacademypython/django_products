from django.contrib import admin
from product.models import Product, Company, Sales
import csv
from django.http import HttpResponse


# Register your models here.

class SalesInlineAdmin(admin.StackedInline):
    model = Sales
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SalesInlineAdmin]
    actions = ["make_actions", "export_as_csv"]
    list_filter = ["expire_date", "name"]
    search_fields = ["name", "company__name", "user__first_name", "user__last_name"]
    list_display = ["name", "quantity", "user", "company", "price"]

    def make_actions(self, request, queryset):
        for obj in queryset:
            obj.name += " Updated!!"
            obj.save()

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format('products')
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "total_price", "company", "salesman"]
