from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import *

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status="Pending").count()
    context = {'orders':orders,'customers':customers,'total_orders':total_orders,'total_delivered':total_delivered,'total_pending':total_pending}
    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

def customer(request):
    return render(request, 'accounts/customer.html')