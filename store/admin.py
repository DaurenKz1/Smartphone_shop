from django.contrib import admin
from .models import Brand, Category, Smartphone


class AddBrand(admin.ModelAdmin):
	list_display = ['name', 'slug', 'logo']
	prepopulated_fields = {'slug': ('name', )}

admin.site.register(Brand, AddBrand)

class AddCategory(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, AddCategory)

class AddSmartphone(admin.ModelAdmin):
    list_display = ['name','price', 'stock', 'description', 'screen_size', 'battery_capacity', 'ram', 'storage', 'camera_resolution', 'processor', 'totalreview', 'totalrating']
    list_filter = ['brand', 'category', 'created_at', 'updated_at']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Smartphone, AddSmartphone)

