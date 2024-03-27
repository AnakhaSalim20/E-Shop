from django.contrib import admin

from myapp import models

# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Complaint)
admin.site.register(models.CartItem)
admin.site.register(models.Payments)
admin.site.register(models.Review)
admin.site.register(models.Paymentz)
admin.site.register(models.Order)
