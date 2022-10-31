from multiprocessing import context
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from accounts.models import *
from .models import *
from .forms import *
from .filters import *

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

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myfilter = OrderFilter(request.GET,queryset=orders)
    orders = myfilter.qs
    context={'customer':customer,'orders':orders,'myfilter':myfilter}
    return render(request, 'accounts/customer.html',context)

def createOrders(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        formset = OrderFormSet(request.POST,instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {"item":order}
    return render(request,'accounts/delete.html',context)