from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout

def HomeView(request):
    return render(request,'vacciapp/home.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('viewSlot')
    return render(request, 'vacciapp/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registered Successfully')
            user = form.save()
            return render(request,'vacciapp/login.html')
    context = {
        'form' : form,
    }
    return render(request,'vacciapp/register.html',context)

    
def profile(request):
    try:
        add = Customer.objects.filter(user=request.user)
    except:
        pass
    form = CustomerProfileForm()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            aadhar = form.cleaned_data['aadhar']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            vtaken = form.cleaned_data['vtaken']
            email = request.user.email
            customer_profile = Customer(user=usr,name=name,phone=phone,aadhar=aadhar,age=age,gender=gender,address=address,city=city,state=state,pincode=pincode,vtaken=vtaken,email=email)
            msg = "Profile Updated!!!"
            customer_profile.save()
    context = {
        'form' : form,
        'add' : add
    }
    return render(request,'vacciapp/profile.html',context)

def viewSlot(request):
    pincodes = Customer.objects.filter(user=request.user).values('pincode')
    l = len(pincodes)
    if l>0:
        userPincode = pincodes[l-1].get('pincode')
        slots = Slot.objects.filter(pincode=userPincode)
        vtype = Slot.objects.values('vtype')
        context = {
            'slots' : slots,
        }
        return render(request,'vacciapp/viewSlot.html',context)
    else:
        return redirect ('profile')

def selectSlot(request,pk):
    user = request.user
    slot = Slot.objects.get(pk=pk)
    context = {
        'slot' : slot,
    }
    return render(request,'vacciapp/selectSlot.html',context)

def orderSlot(request,pk):
    add = Customer.objects.filter(user=request.user)
    usr = request.user
    slot = Slot.objects.get(pk=pk)
    if request.method == 'POST':
        print("OK")
        custid = request.POST.get('custid')
        customer = Customer.objects.get(id=custid)     
        Booking(user=usr,customer=customer,slot=slot).save()
        return redirect ('bookedSlot')
    context = {
        'slot' : slot,
        'add':add,
    }
    return render(request,'vacciapp/orderSlot.html',context)

def bookedSlot(request):
    bs = Booking.objects.filter(user=request.user)
    context = {
        'bs' : bs,
    }
    return render(request,'vacciapp/bookedSlot.html',context)

def adminViewPincode(request ):
    customers = Customer.objects.all()
    pincodes = Customer.objects.values('pincode')
    print(pincodes)
    pins = []
    count = []
    pincd = []
    for i in pincodes:
        pins.append(i.get('pincode'))
    
    done = []
    pin_dict = dict()
    for j in pins:
        if j in done:
            continue
        else:
            occ = pins.count(j)
            pin_dict[f'{j}'] = occ

    pin_sort = sorted(pin_dict.items(),key=lambda x: x[1], reverse=True)

    pincd = []
    count = []
    for k in pin_sort:
        pincd.append(k[0])
        count.append(k[1])
    # print(pincd)
    # print(count)

    slots = Slot.objects.all()

    context = {
        'customers' : customers,
        'pincd' : pincd,
        'count' : count,
        'slots' : slots
    }
    return render(request,'vacciapp/adminViewPincode.html',context)
    

def adminCreateSlot(request,pin):
    form = AdminCreateSlotForm()
    if request.method == 'POST':
        form = AdminCreateSlotForm(request.POST)
        if form.is_valid():
            vtype = form.cleaned_data['vtype']
            date = form.cleaned_data['date']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            addMap = form.cleaned_data['addMap']
            create_slot = Slot(vtype=vtype,date=date,address=address,city=city,state=state,pincode=pincode,addMap=addMap)
            create_slot.save()
    context = {
        'form' : form,
        
    }
    return render(request,'vacciapp/adminCreateSlot.html',context)

def adminUpdateSlot(request,pk):
    slot = Slot.objects.get(id=pk)
    form = AdminCreateSlotForm(instance=slot)
    form = AdminCreateSlotForm()
    context = {
        'form' : form
    }
    if request.method == 'POST':
        form = AdminCreateSlotForm(request.POST,instance=slot)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'vacciapp/adminCreateSlot.html',context)


def adminCompletedSlot(request):
    bs = Booking.objects.all()
    context = {
        'bs' : bs,
    }
    return render(request,'vacciapp/adminCompletedSlot.html',context)

def adminUpdateStatus(request,pk):
    bs = Booking.objects.get(id=pk)
    bsn = Booking.objects.filter(id=pk)
    if request.method == 'POST':
        setstatus = request.POST.get('setstatus')
        print(setstatus)
        status = setstatus
        bs.status = setstatus
        bs.save()
        return redirect ('/')
    context = {
        'bsn' : bsn
    }
    return render(request,'vacciapp/adminUpdateStatus.html',context)


