from django.db import models
import random
import string
from datetime import date,timedelta





def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_user_generator(size=3, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
# Create your models here.

class Customer(models.Model):
    full_name = models.CharField(max_length=255,blank=False)
    user = models.CharField(max_length=255,default = (f'#{random_string_generator()}').upper(),unique=False)    
    organization = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    designation = models.CharField(max_length=255,blank=True)
    passport_id_number = models.CharField(max_length=255,blank=True)
    location = models.CharField(max_length=255,blank=True)
    phone_number = models.IntegerField(blank=False, help_text='Contact phone number',null=True)
    nationality = models.CharField(max_length=155,blank=True)
    remarks = models.CharField(max_length=255,blank=True)
    traval_agent = models.CharField(max_length=255,blank=True)
    bill_setteled_by = models.CharField(max_length=255,blank=True)
    booked_by = models.CharField(max_length=255,blank=False)
    check_in = models.DateTimeField(auto_now=False,null=True)
    check_out = models.DateTimeField(auto_now=False,null=True)
    main_id = models.ImageField(upload_to="customer/id",null=True,blank=True)


    
  
    
    def format_date(obj):
        return obj.check_in.strftime('%d %b %Y %H:%M')
    
    



    def __str__(self):
        return self.full_name
class Additional_id(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    add_id = models.ImageField(upload_to="customer/add_id",null=True,blank=True)
    
class Grouped_room(models.Model):
    title = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.title



class Room(models.Model):
    room_status = (
        ("available", "available"),
        ("booked","booked"),
        ("not-confirm","confirm"),
        ("cancled","cancled"),
        ("cleaning", "cleaning"),
        ("maintenance", "maintenance"),)
    room_number = models.CharField(max_length=255)
    group = models.ForeignKey(Grouped_room,on_delete=models.CASCADE,blank=True)
    price_pernight = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=room_status, default="available")
    

    def __str__(self):
        return f"{self.room_number}"


class Booked(models.Model):
    customer_details = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    room_id = models.ManyToManyField(Room, blank=True)
    number_of_days = models.IntegerField(default=0,null=True ,blank=True)
    booked_date = models.DateTimeField(auto_now_add=True,null=True)
    child = models.IntegerField(default=0,null=True,blank=True)
    male_number = models.IntegerField(default=0,null=True,blank=True)
    female_number = models.IntegerField(default=0,null=True,blank=True)
    other_gender = models.IntegerField(default=0,null=True,blank=True)
    status = models.BooleanField(default=False)
    class Meta:
        ordering =["-booked_date"]
        
    @property
    def total_room(self):
        total_room = self.room_id.objects.all()
        return total_room

    def __str__(self):
        return f'{self.customer_details}'

    @property
    def business_days(self):
        holidays = Customer.objects.values_list('check_in', flat=True)
        oneday = timedelta(days=1)
        # print(oneday)
        dt = self.booked_date.date()
        # print("this is dt",dt)
        total_days = 0
        while (dt <= date.today()):
            if not dt.isoweekday() in (6, 7) and dt not in holidays.values():
                total_days += 1
            dt += oneday
        return total_days






class Advance_payment(models.Model):
    Payment_mode = (
        ("Esewa", "Eswa"),
        ("Khalti", "Khalti"),
        ("Bank Transfer", "Bank Transfer"),
        ("Cash", "Cash"),
        ("Other", "Other"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    Advance_amount = models.CharField(max_length=255, blank=True)
    payment_day = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(
        max_length=255, choices=Payment_mode, default="available")
    remarks = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.customer.full_name


class Customer_list(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    # advance = models.ManyToManyField(Advance_payment,blank=True,null=True)
    checkin = models.DateTimeField(auto_now_add= True,null=True)
    checkout = models.CharField(max_length=255, default="stay")
    bookd_roooms = models.ForeignKey(
        Booked, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.customer.full_name

    @property
    def total_amount(self):
        total_amt = 0.0
        data = Advance_payment.objects.filter(customer=self.customer.id)
        print("this is data:",data)
        for d in data:
            total_amt += float(d.Advance_amount)
        if total_amt == 0.0:
            a = 0
        else:
            a = total_amt
        return a

    @property
    def total_resturent_amount(self):
        res_total = 0.0
        query = Order.objects.filter(
            customer=self.customer).all()
        for q in query:
            res_total += float(q.total)

        return res_total

    @property
    def room_cost(self):
        res_total = 0.0
        query = self.bookd_roooms.room_id.all()

        for q in query:
            res_total += float(q.price_pernight)

        return res_total

    @property
    def all_rooms(self):
        a = self.bookd_roooms.room_id.all()
        return a


class Ch_out(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    remaing_balance = models.FloatField(default=0,null=True)
    # resturent_bill = models.FloatField()
    room_bill = models.FloatField(default=0,null=True)
    # bar_bill = models.ForeignKey(Bar_items,on_delete=models.CASCADE)
    resturent_discount = models.FloatField(blank=True)
    # bar_discount = models.FloatField
    vat = models.BooleanField(default=False)
    room_discount = models.FloatField(blank=True)
    remarks = models.CharField(max_length=255 ,blank=True)

    def __str__(self) -> str:
        return self.customer.full_name

    @property
    def rem_bln(self):
        rem = self.remaing_balance
        if rem is None:
            rem =0
        else:
            rem = self.remaing_balance
        return rem
     
    

    @property
    def resturent_dic(self):
        return self.resturent_discount

    @property
    def room_dic(self):
        return self.room_discount




class Order(models.Model):
    order_id = models.CharField(max_length=255,default = (f'#{random_string_generator()}').upper(),unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True,null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,blank=True,null=True)
    
    total = models.CharField(max_length=255, null=True ,blank=True)
  
    order_date= models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.order_id}'


    
    @property
    def order_user(self):
        return f'{self.customer.full_name}'



class Non_room_user(models.Model):
    Payment_mode = (
        ("Esewa", "Eswa"),
        ("Khalti", "Khalti"),
        ("Bank Transfer", "Bank Transfer"),
        ("Cash", "Cash"),
        ("Other", "Other"),
    )
    order_id = models.CharField(max_length=255,default = (f'#{random_string_generator()}').upper(),unique=True)
    full_name = models.CharField(max_length=255,)
    phone_number = models.IntegerField()
    email = models.EmailField()
    total = models.FloatField(max_length=255, null=True ,blank=True)
    amount_paid = models.FloatField(default=0)
    remaing_amount = models.FloatField(default=0)
    Payment_mode = models.CharField(max_length=255,choices=Payment_mode,null=True,default="UNPAID")
    order_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    


    def __str__(self):
        return f'{self.order_id } {self.full_name }'