from django.contrib import admin
from .models import *


class Companyadmin(admin.ModelAdmin):
    list_display=('name','address','contact_number','email','website')

class Medicineadmin(admin.ModelAdmin):
    
    list_display=('name','category','company','price','stock','expiry_date','description','ratings','image')

class Customeradmin(admin.ModelAdmin):
    list_display=('user','phone','address','date_of_birth','profile_image')

class Prescriptionadmin(admin.ModelAdmin):
    list_display = ('customer','is_approved','uploaded_at')
    fields=('customer', 'prescription_file', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_prescriptions']
    def approve_prescriptions(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected prescriptions have been approved.")
    approve_prescriptions.short_description = "Approve selected prescriptions"

class Salesadmin(admin.ModelAdmin):
    list_display=('customer','medicine','quantity','total_price','sale_date','payment_method') 

class Feedbackadmin(admin.ModelAdmin):
    list_display=('customer','comments','rating','submitted_at')    

class Symptomadmin(admin.ModelAdmin):
    list_display=('name',)

class Recommendationadmin(admin.ModelAdmin):
    list_display=('symptom','recommended_medicine')  

class InventoryLogadmin(admin.ModelAdmin):
    list_display=('medicine','change','change_date','notes')   

class Doctoradmin(admin.ModelAdmin):
    list_display=('user','specialization','license_number','contact_number','available','profile_image')
     
class Paymentadmin(admin.ModelAdmin):
    list_display=('customer','sales','amount','stripe_charge_id','timestamp')   

class Orderadmin(admin.ModelAdmin):
    list_display=('customer','medicine','total_price','order_date','status')


admin.site.register(Company,Companyadmin)
admin.site.register(Medicine, Medicineadmin)
admin.site.register(Customer,Customeradmin)
admin.site.register(Prescription,Prescriptionadmin)
admin.site.register(Sales,Salesadmin) 
admin.site.register(Feedback,Feedbackadmin)
admin.site.register(Symptom,Symptomadmin)
admin.site.register(Recommendation,Recommendationadmin)
admin.site.register(InventoryLog,InventoryLogadmin)
admin.site.register(Doctor,Doctoradmin)
admin.site.register(Payment,Paymentadmin)
admin.site.register(Order,Orderadmin)

