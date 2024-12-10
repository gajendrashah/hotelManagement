from django.contrib import admin

from roomapp.models import Advance_payment, Booked, Ch_out, Customer, Customer_list, Order, Room

# Register your models here.
admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Booked)
admin.site.register(Customer_list)
admin.site.register(Advance_payment)
admin.site.register(Order)
admin.site.register(Ch_out)