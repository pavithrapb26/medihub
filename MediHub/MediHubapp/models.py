from django.db import models
from django.contrib.auth.models import User



class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(null=False)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    


class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Skincare', 'Skincare'),
        ('Haircare', 'Haircare'),
        ('Pain Relief', 'Pain Relief'),
        ('Vitamins', 'Vitamins'),
        ('General medicine','General medicines'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES) 
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='medicines')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    expiry_date = models.DateField()
    description = models.TextField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average ratings
    image = models.ImageField(upload_to='medicine_images/', null=True, blank=True)
    

    def __str__(self):
        return self.name 
    


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)
    available = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

    
class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='prescriptions')
    prescription_file = models.FileField(upload_to='prescriptions/')
    is_approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription of {self.customer.user.username} - Approved: {self.is_approved}"

class Sales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online', 'Online')])

    def __str__(self):
        return f"Sale of {self.medicine.name} to {self.customer.user.username} on {self.sale_date}"



class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    rating = models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.customer.user.username} - Rating: {self.rating}"
    

class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Recommendation(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='recommendations')
    recommended_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.symptom.name} -> {self.recommended_medicine.name}"
    
class InventoryLog(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    change = models.IntegerField()  
    change_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Inventory change for {self.medicine.name} on {self.change_date}"
    
class Payment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    sales = models.ForeignKey('Sales', on_delete=models.CASCADE, null=True, blank=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of ${self.amount} by {self.customer}"



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered')],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"