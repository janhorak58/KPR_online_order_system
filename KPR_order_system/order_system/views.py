from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Order, Address, Shipping, Book
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def count_total(order):
        total = 0
        books = Book.objects.filter(order=order)
        subtotal = 0
        for book in books:
            subtotal += book.price * book.qty
        
        try:    
            subtotal = subtotal - (order.sale/100)
        except:
            pass
        total += subtotal 
        return total

def home(request):
    if request.user.is_authenticated:
        return redirect("prehled")
    return render(request, "order_system/home.html", {"user":request.user})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect("prehled")
    else:
        if request.method == "GET":
            return render(request, "order_system/home.html", {'user':request.user})
        else:
            user = authenticate(request, username = request.POST["username"], password= request.POST["password"])
            if user is None:
                return render(request, "order_system/home.html", {'user':request.user, "error":"Uživatelské jméno a heslo se neshoduje"})
            else:
                login(request, user)
                return redirect("prehled")

@login_required 
def prehled(request, m=0, y=0, zmena=""):
    if request.user.is_authenticated:
        thisMonth = int(m)
        thisYear = int(y)
        if zmena != "":
            if zmena == "dalsi":
                if m < 12:
                    thisMonth = int(m) + 1
                    thisYear = int(y) 
                else:
                    thisMonth = 1
                    thisYear = int(y) + 1
            else:
                if int(m) > 1:
                    thisMonth = int(m) - 1
                    thisYear = int(y) 
                else:
                    thisMonth = 12
                    thisYear = int(y) - 1
        
        
                    
        elif int(m)==0:
            
            thisMonth = int(datetime.datetime.today().month)
            thisYear = int(datetime.datetime.today().year)
        elif int(y)==0:
            thisYear = int(datetime.datetime.today().year)
            thisMonth = int(m)
        else:
            thisYear = int(y)
            thisMonth = int(m)
                
        orders = Order.objects.filter(month = thisMonth, year=thisYear)

        addresses = Address.objects.all()
        ordersLength = len(orders)
        total = 0
        for order in orders:
            order.total = count_total(order)
            order.save()
            total += order.total
        even_orders = []
        odd_orders = []
        for index, order in enumerate(orders):
            if index % 2 == 0:
                even_orders.append(order)
            else:
                odd_orders.append(order)
                
        # even_orders = reversed(even_orders)  
        # odd_orders = reversed(odd_orders)  
        return render(request, "order_system/prehled.html", {'user':request.user, 'even_orders':even_orders,  'odd_orders':odd_orders, "addresses":addresses, "year":int(thisYear), "month":int(thisMonth), "ordersLength":int(ordersLength), "total":total})
    else:
        return redirect("home")
        
@login_required
def searchOrder(request):
    if request.method == "POST":
        d = 0
        m = 0
        y = 0
        try:
            d = int(request.POST["den"])
        except:
            pass
        
        try:
            m = int(request.POST["mesic"])
        except:
            pass
        
        try:
            y = int(request.POST["rok"])
        except:
            pass
        
        
        
        if y == 0 and m == 0 and d == 0:
            return redirect("prehled")
        
        elif y==0 and m == 0:
            orders = Order.objects.filter(day=d)
        elif y==0 and d == 0:
            orders = Order.objects.filter(month=m)
        elif m==0 and d == 0:
            orders = Order.objects.filter(year=y)     
        elif y==0:
            orders = Order.objects.filter(day=d, month=m)
        elif m==0:
            orders = Order.objects.filter(year=y, day=d)
        elif d==0:
            orders = Order.objects.filter(year=y, month=m)
        else:
            orders = Order.objects.filter(year=y, month=m, day=d)
        
        
        return render(request, "order_system/searchOrder.html", {"orders": orders, "month": m, "day":d, "year":y, "ordersLength":len(orders), "NoParams":False})
    
    else:
        return render(request, "order_system/searchOrder.html", {"noParams": True})
        
            
            
    
@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)        
    return redirect("home")

@login_required
def addOrder(request):
    if request.method == "GET":
        return render(request, "order_system/addOrder.html", {'user':request.user})
    else:
        order = Order.objects.create()
        order.save()
        return redirect('editOrder', order.id)
    
    
@login_required
def deleteOrder(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=pk)
        if order:
            order.delete()
    return redirect('prehled')

@login_required
def detailOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    addresses = Address.objects.filter(shipping=order.shipping)
    books = Book.objects.filter(order = order)
    total = 0
    order.total = count_total(order)
    order.save()
    return render(request, "order_system/detailOrder.html", {'user':request.user, 'order': order, 'addresses':addresses, "books":books, "total":order.total})


@login_required
def addBook(request, pk):
    order = get_object_or_404(Order, id = pk)
    book = Book.objects.create()
    book.order = order
    book.save()
    order.total = count_total(order)
    order.save()
    return redirect('editBook', pk, book.id)
    
    
@login_required
def editBook(request, pk, sk):
    if request.method == "GET":
        order = get_object_or_404(Order, id = pk)
        book = get_object_or_404(Book, id = sk)
        try:
            book.price = float(book.price)
        except:
            book.price = 0
            
        try:
            book.qty = int(book.qty)
        except:
            book.qty = 1
        return render(request, "order_system/editBook.html", {'user':request.user, 'order':order, 'book':book, "bookNum":sk})

    else:
        order = get_object_or_404(Order, id = pk)
        if order:


            book = get_object_or_404(Book, id = sk)
            book.name = request.POST["name"]
            book.author = request.POST["author"]
            try:
                book.price = float(request.POST["price"])
            except:
                book.price = 0
            try:
                book.qty = int(request.POST["qty"])
            except:
                book.qty = 1
            
            book.save()
            order.total = count_total(order)
            order.save()
            # return render(request, "order_system/editBook.html", {'user':request.user, 'order':order, 'book':book, "bookNum":int(sk)})
            return redirect('detailOrder', order.id)

                
        else:
    
            return redirect("home")

def deleteBook(request, pk, sk):
    if request.method == "POST":
        
        book = get_object_or_404(Book, id = sk)
        order = get_object_or_404(Order, id = pk)
        if book.order == order:
            book.delete()
        return redirect('detailOrder', order.id)
        
        
@login_required
def editOrder(request, pk):
    if request.method == "GET":
            order = get_object_or_404(Order, id = pk)
            addresses = Address.objects.filter(shipping=order.shipping)
            books = Book.objects.filter(order = order)
            
            return render(request, "order_system/editOrder.html", {'user':request.user, 'order': order, 'addresses':addresses, "books":books})
    else: 
        order = get_object_or_404(Order, id = pk)

        if order:
            order.number = 0
            try:
                order.number = int(request.POST['number'])
            except:
                pass
            order.paid = False
            try:
                if request.POST['paid']:
                    
                    order.paid = True
            except:
                pass
            if order.paid:
                order.completed_date = datetime.datetime.now()
                
            order.payment_method = request.POST["payment_method"]
            order.sale = 0
            
            if request.POST["sale"]:
                order.sale = int(request.POST["sale"])
        
            order.note = request.POST["note"]
            order.state = request.POST["state"]
            order.through_option = request.POST["through_option"]
            
            try:
                order.faktura = request.FILES["faktura"]
            except:
                pass
            try:
                request.FILES["dodaci_list"]
                order.dodaci_list = request.FILES["dodaci_list"]
            except:
                pass            
            shipping = Shipping.objects.create()
            shipping.shipping_type = request.POST["shipping_type"]
            try:
                if request.POST["FisD"]:
                    shipping.FisD = True
                    print("ciiodfhsiu:   ", request.POST["FisD"])
            except:
                
                shipping.FisD = False
            shipping.save()
            
            
            f_address = Address.objects.create()
            f_address.jmeno = request.POST["f_jmeno"]
            f_address.mesto = request.POST["f_mesto"]
            f_address.ulice = request.POST["f_ulice"]
            f_address.psc = request.POST["f_psc"]
            f_address.shipping = shipping
            
            if not shipping.FisD:
                d_address = Address.objects.create()
                d_address.jmeno = request.POST["d_jmeno"]
                d_address.mesto = request.POST["d_mesto"]
                d_address.ulice = request.POST["d_ulice"]
                d_address.psc = request.POST["d_psc"]
                d_address.shipping = shipping
                d_address.save()
            
            
            f_address.save()
            order.shipping = shipping
            order.total = count_total(order)
            
            order.save()
        
        return redirect('detailOrder', order.id)
    


    