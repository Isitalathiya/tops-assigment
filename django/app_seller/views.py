from django.shortcuts import render
from app_seller.models import*
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.
def seller_index(request):
    try:
        request.session['email']
        session_user_data=seller_User.objects.get(request.session['email'])
    except:
        return render(request,"seller_index.html")

def seller_register(request):
    if request.method=="POST":
        try:
            seller_User.objects.get(email=request.POST['email'])
            return render(request,"seller_register.html",{'msg':"User Already Exist"})
        except:
           if request.POST['pass']==request.POST['cpass']:
                global temp
                temp = {
                    'fname':request.POST['fname'],
                    'email':request.POST['email'],
                    'pass':make_password(request.POST['pass'])
                    
                    
                }
                global votp

                votp=random.randint(100000,999999)
                subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
                message = f'your OTP is {votp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,"seller_otp.html")

               
               
           else:
                return render(request,"seller_register.html",{'msg':"Password And Confirm Password Not Match"})
    else:
        return render(request,"seller_register.html")
def seller_otp(request):
    if request.method=="POST":
        if votp==int(request.POST['otp']):
            seller_User.objects.create(
                fullname=temp['fname'],
                email=temp['email'],
                password=temp['pass']
            )
            return render(request,"seller_login.html",{'msg':"Registration Successful"})
        else:
            return render(request,"seller_otp.html",{'msg':"Otp Incorrect"})
    else:
        return render(request,"seller_otp.html")
    
def seller_login(request):
    if request.method=="POST":
        try:
            user_data=seller_User.objects.get(email=request.POST['email'])
            if check_password(request.POST["pass"],user_data.password):
                request.session['email']=request.POST['email']
                request.session['name']=user_data.fullname
                session_user_data=seller_User.objects.get(email=request.session['email'])
                return render(request,"seller_index.html",{"session_user_data":session_user_data})
            else:
                return render(request,"seller_login.html",{"msg":"Invalid Password"})
        except:
            return render(request,"seller_login.html",{"msg":"Account Not Exist Please Register"})
    else:
        return render(request,"seller_login.html")

def seller_forgot_password(request):
    if request.method=="POST":
        try:
            user_data=seller_User.objects.get(email=request.POST['email'])
            request.session['e_email']=request.POST['email']
            global votp
            votp=random.randint(100000,999999)
            subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
            message = f'your OTP is {votp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,"seller_forgot_otp.html")
            
        except:
             return render(request,"seller_forgot_password.html",{"msg":"Email Is Invalid !!"})
    else:
        return render(request,"seller_forgot_password.html")
    
    
def seller_forgot_otp(request):
    if request.method=="POST":
        global votp
        if votp ==int(request.POST['otp']):
            return render(request,"seller_reset_password.html",{'msg':"Registration Successful !!"})
        else:
            return render(request,"seller_forgot_otp.html",{'msg':"Otp Incorrect !!"})
    else:
        return render(request,"seller_forgot_otp.html")
        
def seller_reset_password(request):
    if request.method=="POST":
        if request.POST['pas']==request.POST['cpas']:
            user_data=seller_User.objects.get(email=request.session['e_email'])
            user_data.password=make_password(request.POST["pas"])
            user_data.save()
            return render(request,"seller_index.html",{"msg":"Password Changed !!"})
        else:
            return render(request,"seller_reset_password.html",{"msg":"Password And Confirm-Password Not Match !!"})
    else:
        return render(request,"seller_reset_password.html")
    
   
def seller_profile(request):
    try:
        request.session['email']
        session_user_data=seller_User.objects.get(email=request.session['email'])
        if request.method=="POST":
            user_data=seller_User.objects.get(email=request.session['email'])
            
            if request.POST['pass']:
                if check_password(request.POST["opass"],user_data.password):
                    if request.POST['pass']==request.POST['cpass']:
                        user_data=seller_User.objects.get(email=request.session['email'])
                        user_data.fullname=request.POST['fname']
                        user_data.password=make_password (request.POST['pass'])
                        try:
                            request.FILES['pic']
                            user_data.profilepic=request.FILES['pic']
                            user_data.save()
                        except:
                            user_data.save()
                    
                    
                        return render(request,"seller_profile.html",{"user_data":user_data,"msg":"Profile Updated Succsefully !!","session_user_data":session_user_data})
                    else:
                        user_data=seller_User.objects.get(email=request.session ['email'])
                        return render(request,"seller_profile.html",{"user_data":user_data,"msg":"Password And Confirm Password Not Match !!","session_user_data":session_user_data}) 
                else:
                    return render(request,"seller_profile.html",{"user_data":user_data,"msg":"Old Password Not Match!!","session_user_data":session_user_data })
            else:
                user_data=seller_User.objects.get(email=request.session['email'])
                user_data.fullname=request.POST['fname']
                try:
                    request.FILES['pic']
                    user_data.profilepic=request.FILES['pic']
                    user_data.save()
                except:
                    user_data.save()
                return render(request,"seller_profile.html",{"user_data":user_data,"msg":"Profile Updated Succsefully!","session_user_data":session_user_data })
        else:
            user_data=seller_User.objects.get(email=request.session['email'])
            return render(request,"seller_profile.html",{"user_data":user_data,"session_user_data":session_user_data})
    except:
         return render(request,"seller_index.html")
    
def seller_logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request,"seller_index.html")
    except:
        return render(request,"seller_index.html")
    


def addproduct(request):
    if request.method == "POST":
        seller_data=seller_User.objects.get(email=request.session['email'])
        try:
            request.FILES['pic']
            AProduct.objects.create(
                name=request.POST['pname'],
                price=request.POST['price'],
                description=request.POST['desc'],
                image=request.FILES['pic'],
                seller=seller_data
                
            )
        except:
            AProduct.objects.create(
                name=request.POST['pname'],
                price=request.POST['price'],
                description=request.POST['desc'],
                seller=seller_data
            )

        return render(request,"addproduct.html",{'msg':"add product Successful"})
        
    else:
        return render(request,"addproduct.html")
    



