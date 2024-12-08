from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('signin/',views.signin,name='signin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('customer_login/',views.customer_login,name='customer_login'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('ai-suggestion/', views.ai_suggestion, name='ai_suggestion'),
    path('medicinelist/',views.list_medicines,name='medicinelist'),
    path('medicine/<int:medicine_id>/',views.medicine_detail,name='medicine_detail'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    path('view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('compare/<str:medicine_name>/', views.compare_brands, name='compare_brands'),
    path('buy-medicines/',views.buy_medicine_list, name='buy_medicines'),
    path('buy-medicine/<int:medicine_id>/', views.buy_medicine, name='buy_medicine'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:category_name>/', views.medicines_by_category, name='medicines_by_category'),
    path('addtocart/<int:medicine_id>/',views.add_to_cart,name="add_to_cart"),
    path('cart/', views.cart, name='cart'),
    path('order-medicine/', views.order_medicine, name='order_medicine'),
    path('category/<str:category>/', views.view_category, name='view_category'),
    path('order/<int:medicine_id>/', views.order_now, name='order_now'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('sales-history/', views.sales_history, name='sales_history'),
    path('saleshistory/', views.saleshistory, name='saleshistory'),
    path('invoice/<int:sale_id>/', views.invoice_details, name='invoice_details'),
    path('profile/', views.profile_view, name='profile'),
    path('search-medicine/', views.search_medicine, name='search_medicine'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
]
    



