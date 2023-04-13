from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from .forms import NewUserForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this

import razorpay
client = razorpay.Client(auth=("rzp_test_FfNuJ70du4uyfg", "MzdZPJIBglvEhhGVryCbqXDe"))
dorder_id=''
def newsletter(email):
	newsletter=Newsletter(email=email)
	newsletter.save()
	
	
# Create your views here.
def home(request):
    song=Song.objects.filter(price=0).order_by('-date')
    if request.method=="POST":
	    email=request.POST.get('email')
	    newsletter(email)
    return render(request, "musico-master/index.html",{'song':song,})
def blog(request):
	

	if request.method=="POST":
	  email=request.POST.get('email')
	  newsletter(email)
	blog=Blog.objects.filter(publish=True).order_by('-date')
	tags=Tags.objects.all()

	genere=Genre.objects.all()
	tag=request.GET.get('tag')
	if tag!=None:
		blog=Blog.objects.filter(publish=True,tags=tag).order_by('-date')
	category=request.GET.get('category')
	if category!=None:
		blog=Blog.objects.filter(publish=True,genere=category).order_by('-date')

	
	
	return render(request, "musico-master/blog.html",{'blog':blog,'genere':genere,'tags':tags,})
def blogdetails(request,**args):
	tags=Tags.objects.all()
	blogdetails=get_object_or_404(Blog,**args)
	genere=Genre.objects.all()
	comments=Comment.objects.filter(post=blogdetails,is_parent=True).order_by('-created_date')
	commentcount=comments.count()
	if request.method=="POST":
	  try:
	    user=request.user
	    comment=request.POST.get("comment")
	    com=Comment(text=comment,author=user,post=blogdetails)
	    com.save()
	  except:
	      try:
	        reply=request.POST.get('reply')
	        print(reply)
	        commentid=request.POST.get('commentid')
	        print(commentid +"=============================================")
	        parent_obj=Comment.objects.get(id=commentid)
	        comrep=Comment(text=reply,author=user,post=blogdetails,parent=parent_obj,is_parent=False)
	        comrep.save()
	      except:
	          try:
	            email=request.POST.get('email')
	            newsletter(email) 
	          except:
	            return redirect(f'/blog/{blogdetails.url}')
	return render(request, "musico-master/single-blog.html",{'blogdetails':blogdetails,'comments':comments,'commentcount':commentcount,'genere':genere,'tags':tags,})
  
@login_required(login_url='/login')
def my_tracks(request):
    if request.method=="POST":
	    email=request.POST.get('email')
	    newsletter(email)
    
    freetracks=Song.objects.filter(price=0)
    luser=request.user
    paidtracks=Song.objects.filter(user=luser)
    return render(request,'musico-master/track.html',{'freetracks':freetracks,'paidtracks':paidtracks})
def tracks(request):
    
  tracks=Song.objects.all()
    
  return render(request,'musico-master/products.html',{'tracks':tracks})

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        desc=request.POST.get('message')
        contact=Contact(name=name,email=email,subject=subject,desc=desc)
        contact.save()
        return redirect ('/')
      
    return render(request,'musico-master/contact.html')

@login_required(login_url='/login')
def product(request,id):
    user=request.user
    product=get_object_or_404(Song,id=id)
    prdtpr=int(product.price)*100
    prdtnm=product.song_name
    prdtid=product.id

    data = { "amount": int(product.price)*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    payment_order_id=payment['id']
    user=request.user
    order=Order(product_name=product,order_id=payment_order_id,user=user,paid_amount=product.price,product_id=prdtid)
    
    if len(Order.objects.filter(product_id=prdtid))!=0:
	      Order.objects.filter(product_id=prdtid).update(order_id=payment_order_id) 
	      
    else:
	      order.save()
    return render(request, 'musico-master/main.html',{'payment':payment,'prdtpr':prdtpr,'prdtnm':prdtnm,prdtid:'prtid','order_id':payment_order_id,'product':product})


@csrf_exempt
def verify(request):

  if request.method=="POST":
    payment_id=request.POST.get('razorpay_payment_id')
    order_id=request.POST.get("razorpay_order_id")
    signature=request.POST.get("razorpay_signature")

  if signature!=None:
    
    dorder_id=order_id
    Order.objects.filter(order_id=order_id).update(signature=signature,paid=True)
    luser=request.user
    order=get_object_or_404(Order,order_id=dorder_id)
    song=Song.objects.get(id=order.product_id)
    song.user.add(luser)
    song.save()
    
    return render (request,'musico-master/succes.html',{'order_id':order_id})
  else:
	  return render(request,'musico-master/failure.html')
	  


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()

	return render (request=request, template_name="main/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})
@login_required(login_url='/login')
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")
def search(request):
	if request.method=="POST":
		search=request.POST.get('search')
		blog=Blog.objects.filter(publish=True,title__icontains=search,body__icontains=search).order_by('-date')
		tracks=Song.objects.filter(song_name__icontains=search).order_by('-date')
		blogcont=blog.count
		trckcont=tracks.count
	return render(request,"musico-master/search.html",{'blog':blog,'tracks':tracks,'blogcont':blogcont,'trckcont':trckcont})

def about(request):
	return render(request,"musico-master/about.html")
def error404(request,exception):
    return render(request,'404.html',exception)