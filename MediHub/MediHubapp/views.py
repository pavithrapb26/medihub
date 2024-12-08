from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Medicine, Symptom, Recommendation, Customer,Prescription,Doctor,Payment,Sales,Order
from .forms import PrescriptionUploadForm
from django.urls import reverse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request,'home.html')
def signin(request):
    return render(request,'signin.html')
@login_required
def customersignin(request):
    return render(request,'customersignin.html') 
# def dashboard(request):
#     return render(request,"dashboard.html") 
def dashboard(request):
    # Fetch the first medicine (or any other valid medicine object)
    # medicine = Medicine.objects.first()  # or .get(id=some_id)
    
    # if not medicine:
    #     # Handle the case where no medicine is available
    #     return render(request, 'no_medicines.html')  # Redirect to an appropriate page

    return render(request,'dashboard.html')

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both username and password are required.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard view after login
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login_customer.html')  # Return the login page if not a POST request

def customer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('customer_login')

    return render(request,'register_customer.html')


def ai_suggestion(request):
    if request.method == 'POST':
        symptom_name = request.POST.get('symptom')

        # Check if the symptom exists in the database
        symptom = Symptom.objects.filter(name__iexact=symptom_name).first()

        if not symptom:
            messages.error(request, "No recommendations available for the entered symptom.")
            return render(request, 'ai_suggestion.html')

        # Fetch the associated recommendation
        recommendation = Recommendation.objects.filter(symptom=symptom).first()

        if recommendation:
            context = {
                'recommended_medicine': recommendation.recommended_medicine,
                'symptom': symptom_name
            }
            return render(request, 'ai_suggestion.html', context)
        else:
            messages.error(request, "No recommendations available for the entered symptom.")

    return render(request, 'ai_suggestion.html')


        

      
# def buy_medicine(request, medicine_id=None):
#     try:
#         customer = request.user.customer
#     except Customer.DoesNotExist:
#         messages.error(request, "You need a customer account to buy medicines.")
#         return redirect('dashboard')  # Redirect to dashboard if not a customer

#     # Fetch available medicines (in stock)
#     medicines = Medicine.objects.filter(stock__gt=0)

#     if medicine_id:
#         # If a medicine_id is provided, get that specific medicine
#         suggested_medicine = get_object_or_404(Medicine, id=medicine_id)
#         medicines = [suggested_medicine]  # Override medicine list to show only the suggested medicine

#     if request.method == "POST":
#         selected_medicines = request.POST.getlist('medicines')  # List of selected medicine IDs
#         quantities = request.POST.getlist('quantities')  # Corresponding quantities

#         # Validate input
#         if not selected_medicines or not quantities:
#             messages.error(request, "Please select medicines and quantities.")
#             return redirect('buy_medicine')

#         total_price = 0
#         sales_records = []
#         line_items = []  # For Stripe session creation

#         for i, medicine_id in enumerate(selected_medicines):
#             medicine = get_object_or_404(Medicine, id=medicine_id)
#             quantity = int(quantities[i])

#             if quantity <= 0 or quantity > medicine.stock:
#                 messages.error(
#                     request,
#                     f"Invalid quantity for {medicine.name}. Available stock: {medicine.stock}."
#                 )
#                 return redirect('buy_medicine')

#             # Calculate total price and prepare Stripe line items
#             total_price += quantity * medicine.price
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': medicine.name,
#                     },
#                     'unit_amount': int(medicine.price * 100),  # Convert price to cents
#                 },
#                 'quantity': quantity,
#             })

#         # Create a Stripe Checkout Session
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=request.build_absolute_uri('/payment/cancel/'),
#             )
#             return redirect(checkout_session.url)
#         except stripe.error.StripeError as e:
#             messages.error(request, f"Stripe error: {e}")
#             return redirect('buy_medicine')

#     return render(request, 'buy_medicine.html', {'medicines': medicines})





# def buy_medicine(request):
#     # Fetch medicines and their companies
#     medicines = Medicine.objects.all()
#     return render(request, 'buy_medicine.html', {'medicines': medicines})
# def medicine_detail(request, medicine_id):
#     medicine = get_object_or_404(Medicine, id=medicine_id)
#     companies = medicine.companies.all()  # Assuming a Many-to-Many relationship with companies

#     if request.method == "POST":
#         # Your payment code here (same as previous implementation)
#         selected_medicine = medicine
#         quantity = int(request.POST.get('quantity', 1))

#         if quantity <= 0 or quantity > selected_medicine.stock:
#             messages.error(request, f"Invalid quantity for {selected_medicine.name}. Available stock: {selected_medicine.stock}.")
#             return redirect('medicine_detail', medicine_id=medicine.id)

#         total_price = quantity * selected_medicine.price
#         line_items = [{
        #     'price_data': {
        #         'currency': 'usd',
        #         'product_data': {
        #             'name': selected_medicine.name,
        #         },
        #         'unit_amount': int(selected_medicine.price * 100),  # Convert price to cents
        #     },
        #     'quantity': quantity,
        # }]
        
        # # Stripe checkout session
        # checkout_session = stripe.checkout.Session.create(
        #     payment_method_types=['card'],
        #     line_items=line_items,
        #     mode='payment',
        #     success_url=request.build_absolute_uri('/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
        #     cancel_url=request.build_absolute_uri('/payment/cancel/'),
        # )

        # return redirect(checkout_session.url)

    # return render(request, 'medicine_detail.html', {'medicine': medicine, 'companies': companies})
def list_medicines(request):
    medicines = Medicine.objects.prefetch_related('company').all()
    return render(request,'medicineList.html',{'medicines': medicines})

def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request,'medicine_detail.html',{'medicine': medicine})

# Buy medicine view (as per your existing Stripe integration)
# def buy_medicine(request, medicine_id):
#     # Ensure the user is a customer
#     try:
#         customer = request.user.customer
#     except Customer.DoesNotExist:
#         messages.error(request, "You need a customer account to buy medicines.")
#         return redirect('dashboard')

#     medicine = get_object_or_404(Medicine, id=medicine_id)

#     if request.method == "POST":
#         quantity = int(request.POST.get('quantity', 1))

#         if quantity <= 0 or quantity > medicine.stock:
#             messages.error(request, f"Invalid quantity for {medicine.name}. Available stock: {medicine.stock}.")
#             return redirect('medicine_detail', medicine_id=medicine_id)

#         total_price = quantity * medicine.price
#         line_items = [{
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {'name': medicine.name},
#                 'unit_amount': int(medicine.price * 100),  # Convert to cents
#             },
#             'quantity': quantity,
#         }]

#         # Create Stripe session
#         import stripe
#         stripe.api_key = 'your_stripe_secret_key'
    #     try:
    #         checkout_session = stripe.checkout.Session.create(
    #             payment_method_types=['card'],
    #             line_items=line_items,
    #             mode='payment',
    #             success_url=request.build_absolute_uri('/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
    #             cancel_url=request.build_absolute_uri('/payment/cancel/'),
    #         )
    #         return redirect(checkout_session.url)
    #     except stripe.error.StripeError as e:
    #         messages.error(request, f"Stripe error: {e}")
    #         return redirect('medicine_detail', medicine_id=medicine_id)

    # return render(request, 'buy_medicine.html', {'medicine': medicine})



def upload_prescription(request):
    # Check if the logged-in user is a customer
    if not hasattr(request.user, 'customer'):
        messages.error(request, "Only customers can upload prescriptions.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PrescriptionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.customer = request.user.customer
            prescription.save()
            messages.success(request, "Prescription uploaded successfully!")
            return redirect('view_prescriptions')
        else:
            messages.error(request, "Error uploading prescription. Please try again.")
    else:
        form = PrescriptionUploadForm()
    
    return render(request, 'upload_prescription.html', {'form': form})

def view_prescriptions(request):
    # Check if the logged-in user is a customer
    if not hasattr(request.user, 'customer'):
        messages.error(request, "Only customers can view prescriptions.")
        return redirect('dashboard')

    prescriptions = Prescription.objects.filter(customer=request.user.customer)
    return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

    session = stripe.checkout.Session.retrieve(session_id)
    customer_email = session.customer_details.email
    amount_total = session.amount_total / 100  # Convert cents to dollars

    # Assuming you track customer via email or ID
    customer = get_object_or_404(Customer, user=request.user)
    Payment.objects.create(
        customer=customer,
        amount=amount_total,
        stripe_charge_id=session.payment_intent
    )

    messages.success(request, "Payment successful!")
    return render(request, 'payment_success.html', {'amount': amount_total})



def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')  # Order by name for grouping
    return render(request, 'medicineList.html', {'medicines': medicines})

def compare_brands(request, medicine_name):
    sort_by = request.GET.get('sort', 'price')  # Default to price
    medicines = Medicine.objects.filter(name=medicine_name).order_by(sort_by)
    return render(request, 'compare_brands.html', {'medicines': medicines, 'medicine_name': medicine_name})


def buy_medicine_list(request):
    
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def buy_medicine(request, medicine_id):
    
    try:
        # Ensure the user is a customer
        customer = request.user.customer
    except AttributeError:
        messages.error(request, "You need a customer account to buy medicines.")
        return redirect('dashboard')

    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == "POST":
        # Extract quantity and validate
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0 or quantity > medicine.stock:
            messages.error(request, f"Invalid quantity for {medicine.name}. Available stock: {medicine.stock}.")
            return redirect('buy_medicine', medicine_id=medicine_id)

        # Prepare payment data
        total_price = quantity * medicine.price
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': medicine.name},
                'unit_amount': int(medicine.price * 100),  # Convert price to cents
            },
            'quantity': quantity,
        }]

        # Create Stripe checkout session using your provided code
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
               success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            )
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {e}")
            return redirect('buy_medicine', medicine_id=medicine_id)

    return render(request, 'buy_medicine.html',{'medicine': medicine})

def payment_success(request):
    return render(request,'success.html')

def payment_cancel(request):
    return render(request,'cancel.html')




def category_list(request):
    categories = Medicine.CATEGORY_CHOICES
    return render(request, 'category_list.html', {'categories': categories})
def medicines_by_category(request, category_name):
    medicines = Medicine.objects.filter(category=category_name)
    return render(request, 'medicines_by_category.html', {'medicines': medicines, 'category': category_name})

def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart = request.session.get('cart', [])
    
    cart.append(medicine.id)
    request.session['cart'] = cart
    return redirect('cart')
def cart(request):
    cart_items = Medicine.objects.filter(id__in=request.session.get('cart', []))
    return render(request, 'cart.html', {'cart_items': cart_items})


def order_medicine(request):
    """Display categories for medicine ordering."""
    categories = [choice[0] for choice in Medicine.CATEGORY_CHOICES]
    return render(request, 'order_medicine.html', {'categories': categories})

def view_category(request, category):
    
    medicines = Medicine.objects.filter(category=category)
    return render(request, 'view_category.html', {'medicines': medicines, 'category': category})

def order_now(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        # Validate prescription availability
        customer = request.user.customer
        prescriptions = customer.prescriptions.filter(is_approved=True)
        
        if not prescriptions.exists():
            return render(request, 'order_now.html', {'medicine': medicine, 'error': 'No approved prescriptions found!'})

        # Process order
        quantity = int(request.POST.get('quantity', 1))
        total_price = medicine.price * quantity
        Order.objects.create(
            customer=customer,
            medicine=medicine,
            # quantity=quantity,
            total_price=total_price,
            # order_date=order_date,
            # 
        
        )
        
        medicine.stock -= quantity
        medicine.save()

        return redirect('my_orders')  # Redirect to dashboard or order summary page
    
    return render(request, 'order_now.html', {'medicine': medicine})

def my_orders(request):
    
     customer = request.user.customer  # Get the logged-in customer's profile
     orders = Order.objects.filter(customer=customer).order_by('-order_date')  # Get customer's orders
     return render(request, 'my_orders.html', {'orders': orders})



def sales_history(request):
    customer = request.user.customer  # Get the logged-in customer's profile
    sales = Sales.objects.filter(customer=customer).order_by('sale_date')  # Fetch customer's sales history
    return render(request, 'sales_history.html', {'sales': sales})

def saleshistory(request):
    customer = request.user.customer
    sales = Sales.objects.filter(customer=customer).order_by('sale_date')  # Fetch sales for the logged-in user
    return render(request, 'saleshistory.html', {'sales': sales})

def invoice_details(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, customer=request.user.customer)
    return render(request, 'invoice.html', {'sale': sale})

def profile_view(request):
    customer = request.user.customer  # Get the logged-in customer's profile
    sales = Sales.objects.filter(customer=customer).order_by('-sale_date')  # Get the customer's sales history
    return render(request, 'profile.html', {'customer': customer, 'sales':sales})

def search_medicine(request):
    query = request.GET.get('q')  # Get the search query from the GET request
    medicines = Medicine.objects.filter(name__icontains=query) if query else None
    return render(request, 'search_medicine.html', {'medicines': medicines, 'query': query})

def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        if feedback_text:
            # You can store the feedback in the database if needed.
            # For simplicity, we'll just use a success message.
            messages.success(request, "Your feedback has been submitted successfully. Thank you for your feedback!")
            return redirect('feedback')  # Redirect back to the feedback page
        else:
            messages.error(request, "Feedback cannot be empty. Please enter your feedback.")
    
    return render(request, 'feedback.html')

def about(request):
    return render(request, 'about.html')