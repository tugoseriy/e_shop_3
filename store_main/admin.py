from django.contrib import admin

from .models import Product, Category, UserCart,Sale, Feedback
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserCart)
admin.site.register(Sale)
admin.site.register(Feedback)