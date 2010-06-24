from django.contrib import admin
from foursquare.models import *

class FourSquareUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone', )
admin.site.register(User, FourSquareUserAdmin)

class FourSquareCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullpathname', )
admin.site.register(Category, FourSquareCategoryAdmin)

class FourSquareVenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'phone', )
admin.site.register(Venue, FourSquareVenueAdmin)

class FourSquareCheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue', 'created', )
admin.site.register(CheckIn, FourSquareCheckInAdmin)