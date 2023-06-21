from django.shortcuts import redirect, render
from .models import *
from .utils import generate_pass
import razorpay
from django.http import HttpResponseBadRequest
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.core.mail import send_mail

# Create your views here.

def dashboard(request):
    if request.session.has_key('name'):
        data=Donation.objects.all().order_by('-id')
        return render(request,'admin/dashboard.html',{'data':data})
    return redirect('adminlogin')

def members(request):
    if request.session.has_key('name'):
        models=Registeration.objects.filter(is_verified=False)
        return render(request,'admin/members.html',{'model':models})
    return redirect('adminlogin')

def approvemember(request,id):
    if request.session.has_key('name'):
        model=Registeration.objects.get(id=id)
        model.is_verified=True
        x=generate_pass()
        model.password=x
        model.save()
        send_mail(
                        'Membership approval ',
                        f"Your username is: {model.mobile}\n Your password is: {model.password}",
                        'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                        [model.email],  # TODO: Update this with the recipients mail id
                        fail_silently=False,
                    )
        return redirect('members')        
    return redirect('adminlogin')
     
def rejectmember(request,id):
    if request.session.has_key('name'):
        model=Registeration.objects.get(id=id)
        send_mail(
                        'Membership Not approval ',
                        f"Your memberhip is not approved",
                        'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                        [model.email],  # TODO: Update this with the recipients mail id
                        fail_silently=False,
                    )
        model.delete()
        return redirect('members')        
    return redirect('adminlogin')

def allmembers(request):
    if request.session.has_key('name'):
        model=Registeration.objects.filter(is_verified=True)
        return render(request,'admin/memnbers.html',{'model':model})
    return redirect('adminlogin')
    
def deletemember(request,id):
    if request.session.has_key('name'):
        if request.POST:
            model1=Registeration.objects.get(id=id)
            model1.delete()
            return redirect('allmembers')
    return redirect('adminlogin')
    

def sendmail(request,id):
    if request.session.has_key('name'):
        if request.POST:
            model1=Registeration.objects.get(id=id)
            msg=request.POST.get('message')
            send_mail(
                            'Message from Charity ',
                            f"Your message from Charity is\n{msg}",
                            'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                            [model1.email],  # TODO: Update this with the recipients mail id
                            fail_silently=False,
                        )
            return redirect('allmembers')
        return render(request,'admin/sendmail.html')   
    return redirect('adminlogin')

def alldata(request):
    if request.session.has_key('email'):
        data=Donation.objects.all().order_by('-id')
        return render(request,'user/alldata.html',{'data':data})
    return redirect('login')

def category(request):
    if request.session.has_key('name'):
        mod=CategoryType.objects.all()
        if request.method=='POST':
            model=CategoryType()
            model.name=request.POST['name']
            model.image=request.FILES['image']
            model.description=request.POST['description']
            model.save()
            return redirect('cat')
        return render(request,'admin/category.html',{"mod":mod})
    return redirect('adminlogin')
    

def userindex(request):
    if 'm' in request.session:
        m=request.session['m']
        del request.session['m']
    else:
        m=""
    mod=CategoryType.objects.all()  
    if request.session.has_key('email'): 
        model1=Registeration.objects.get(email=request.session['email'])
        date1=date.today()
        return render(request,'user/index.html',{'mod':mod,'model1':model1,'date':date1})
    else:
        if request.method=='POST':
            model=Registeration()
            model.name=request.POST.get('name')
            model.email=request.POST.get('email')
            model.mobile=request.POST.get('mobile')
            model.save()
            request.session['m']="Request Sent ,wait for admin approval"
            return redirect('userindex')
        date1=date.today()
        return render(request,'user/index.html',{'mod':mod,'date':date1,'m':m})
    
class SuccessView(TemplateView):
    template_name = 'user/success_s.html'


# payment end 
def logout(request):
    if request.session.has_key('email'):
        del request.session['email']
        return redirect('userindex')
    return render(request,'user/index.html')

def adminlogin(request):
    if request.POST:
        try:
            name=request.POST['name']
            print(name)
            password=request.POST['password']
            print(password)
            model=Superuser.objects.get(name=name)
            request.session['name']=name
            if model.password==password:
                return redirect('dashboard')
            else:
                return render(request, "admin/adminlo.html",{'m':"type invalid number and details"})
        except:
            return render(request, "admin/adminlo.html",{'m':"type invalid number and details"})
    return render(request, "admin/adminlo.html")

def login(request):
    if request.POST:
        try:
            no=request.POST['email']
            password=request.POST['password']
            model=Registeration.objects.get(mobile=no,password=password)
            if model:
                request.session['email']=model.email
                return redirect(('userindex'))
            else:
                return render(request, "user/login.html",{'m':"type invalid number and details"})
        except:
            return render(request, "user/login.html",{'m':"type invalid number and details"})
    return render(request, "user/login.html")

def adminlogout(request):
    if request.session.has_key('name'):
        del request.session['name']
        return redirect('adminlogin')
    return render(request,'user/index.html')

def donationcategory(request,id):
    if request.session.has_key('email'): 
        model1=Registeration.objects.get(email=request.session['email'])
        data=CategoryType.objects.get(id=id)
        if request.POST:
            cat=request.POST['category']
            cat1=CategoryType.objects.get(id=cat)
            request.session['username']=model1.pk
            request.session['cat1']=cat1.pk
            request.session['donateAmount']=request.POST['amount']
            return redirect('/razorpayView/') 
        return render(request,'user/donation.html',{'model1':model1,'data':data})

RAZOR_KEY_ID = 'rzp_test_vmxBmKwQ2RVxWn'
RAZOR_KEY_SECRET = '9QSbTgOiZ7vAOS29YN4tfpA0'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['donateAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'user/razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['donateAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)
            #Order Save Code
            model1=Registeration.objects.get(id=request.session['username'])
            cat1=CategoryType.objects.get(id=request.session['cat1'])
            Model = Donation()
            Model.user = model1
            Model.category = cat1
            Model.Amount = request.session['donateAmount']
            Model.save()
            send_mail(
                        'Donation Successfully from Charity ',
                        f"Your donation is successfully done\nThank you so much!!!!",
                        'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                        [model1.email],  # TODO: Update this with the recipients mail id
                        fail_silently=False,
                    )
            del request.session['username']
            del request.session['cat1']
            del request.session['donateAmount']
            # render success page on successful caputre of payment
            return redirect('/success_stripe/')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello123")
       # if other than POST request is made.
        return HttpResponseBadRequest()

