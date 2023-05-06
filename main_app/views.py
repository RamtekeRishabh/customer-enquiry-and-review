from datetime import timedelta
import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from main_app.models import CustEnq,EnqDtl,Review

from django.conf import settings
from django.core.mail import send_mail

from background_task import background


# Create your views here.
def enquiry(request):
    return render(request,"main_app/enquiry.html")

def query_submit(request):
    if request.method=='POST':
        email = request.POST['email']
        # try:
        #     validate_email(email)
        # except ValidationError as e:
        #     print()
        from validate_email import validate_email
        if not validate_email(email):
            msg = "bad email, Please pass the valid email id"
            return render(request, "main_app/enquiry.html", context={"msg": msg})
        else:
            name = request.POST['name'].capitalize()
            contact = request.POST['contact']
            query = request.POST['query']
            qry = CustEnq.objects.create(name=name,email=email,phone=contact,query=query)
            qry.save()

            subject = 'Welcome to Enquiry Portal of <Service Provider>'
            message = f'Hello, {name}, We have received your enquiry. ' \
                      f'We are working on your query and will reply very soon. ' \
                      f'Thank you for showing interest in <Service Provider>.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)
            # print("[query_submit]", message)

            last = CustEnq.objects.last()
            subject = 'Request received on Enquiry Portal of <Service Provider>'
            message = f'Hello, <Service Provider>, You have received enquiry request. ' \
                      f'Check the query here and provide proper response to it. ' \
                      f'http://127.0.0.1:8000/enquiry_detail/{last.id} ' \
                      f'Thank you <br> <Service Provider>.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)
            # print("[enquiry]",message)

            messages.success(request, 'Enquiry submitted successfully')
            return redirect(enquiry)
    else:
        msg = "msg get method not allowed"
        return render(request, "main_app/enquiry.html", context={"msg": msg})

def enquiry_detail(request, id):
    custenq = CustEnq.objects.filter(id=id).first()
    enqdtl = EnqDtl.objects.filter(enqno=id).first()
    # enqdtl = EnqDtl.objects.filter(id=id).first()
    # custenq = CustEnq.objects.filter(id=enqdtl.enqno.id).first()
    if custenq and enqdtl:
        email = custenq.email
        name = custenq.name
        query = custenq.query
        phone = custenq.phone
        qry_response = enqdtl.qry_response
        id = enqdtl.id
        data = {"name":name,"query":query,"email":email,"qry_response":qry_response,"phone":phone,"id":id}
        # print(data)
        return render(request,"main_app/response.html",context={"data":data})
    else:
        msg = "msg Please pass the valid id"
        return render(request, "main_app/response.html", context={"msg": msg})

def response_submit(request,id):
    if request.method=='POST':
        if id is not None:
            response = request.POST['response']
            enqdtl = EnqDtl.objects.filter(id=id).first()
            rvw = Review.objects.filter(enqno=enqdtl.enqno)#
            if enqdtl:
                enqdtl.qry_response = response
                rvw.update(rspno=enqdtl.id) #
                #rvw.rspno = enqdtl.id #
                #rvw.save() #
                enqdtl.save()
                id = enqdtl.enqno.id
                email = enqdtl.enqno.email

                # @background(schedule=60)
                def notify_user(id,email):
                    subject = 'Review to the response Enquiry Portal of <Service Provider>'
                    message = f'Hello, Customer, Provide your review to the response ' \
                              f'http://127.0.0.1:8000/review/{id} ' \
                              f'Thank you <br> <Service Provider>.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list)
                    # print("[response_submit]", email, message)

                notify_user(id,email)

                messages.success(request, 'tag Response submitted successfully')
                # print("enqdtl.enqno.id is ",id)
                return render(request, "main_app/response.html",context={"id":""})
            else:
                msg = "msg Please pass the valid id"
                return render(request, "main_app/response.html", context={"msg": msg})
        else:
            msg = "msg Please pass the valid id"
            return render(request, "main_app/response.html", context={"msg": msg})
    else:
        msg = "msg get not allowed"
        return render(request, "main_app/enquiry.html", context={"msg": msg})

def review(request,id):
    data = id
    # print("data have a id ",id)
    return render(request,"main_app/review.html",context={"data": data})

def review_submit(request,id):
    # print("review submit have a id ", id)
    # print("method is ", request.method)
    if request.method=='POST':
        # satisfied = request.POST['satisfied']
        satisfied = request.POST.get("satisfied")
        # print("satisfied is" ,request.POST.get("satisfied")) #
        # custenq = CustEnq.objects.filter(id=id).first()
        # enqdtl = EnqDtl.objects.filter(enqno=id).first()
        rvw = Review.objects.filter(enqno=id)#
        rvw.update(satisfied=satisfied) #
        # id = enqdtl.id

        # data = {"name": name, "query": query, "email": email, "qry_response": qry_response, "phone": phone, "id": id}



        # messages.success(request, 'tag Your Review submitted successfully')
        msg='tag Your Review submitted successfully'
        return render(request,"main_app/review_submit.html",context={"msg": msg})
    return render(request,"main_app/review_submit.html")