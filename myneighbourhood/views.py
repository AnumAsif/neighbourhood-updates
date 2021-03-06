from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your neighbourhood account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):
    user=request.user
    hoods=Neighbourhood.objects.all()
    return render(request, 'home.html',{'current_user':user, 'hoods':hoods})

@login_required(login_url='/login')
def profile(request, username):
    current_user=request.user
    user=User.objects.get(username=username)
    return render(request,'profile.html',{'current_user':current_user,'user':user})    

@login_required(login_url='/login')
def edit_profile(request):
    user=request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = user
            edit.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileForm()

    return render(request, 'edit_profile.html', {'form':form, 'current_user':user})

@login_required(login_url='/login')
def add_neighbourhood(request):
    user=request.user
    if request.method == 'POST':
        form = HoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = user
            hood.save()
            return redirect('home')
    else:
        form = HoodForm()

    return render(request, 'add_neighbourhood.html', {'form':form, 'current_user':user})

@login_required(login_url='/login')
def hood_details(request, hood_id):
    hood=Neighbourhood.find_neighbourhood(hood_id)
    occupants=Profile.objects.filter(neighbourhood=hood)
    businesses=Business.objects.filter(neighbourhood=hood)
    posts=Post.objects.filter(neighbourhood=hood)
    amenities=Amenity.objects.filter(neighbourhood=hood)

    current_user=request.user
    if request.method=='POST':
        form= PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user.profile
            post.neighbourhood=hood
            post.save()
            return redirect('hood_details', hood_id=hood_id)
    else:
        form=PostForm()        
    return render(request, 'hood_details.html',{'amenities':amenities,'hood':hood,'occupants':occupants, 'businesses':businesses,'posts':posts,'form':form})

@login_required(login_url='/login')
def add_business(request, hood_id):
    user=request.user
    hood=Neighbourhood.find_neighbourhood(hood_id)
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = user
            business.neighbourhood=hood
            business.save()
            return redirect('hood_details', hood_id=hood_id)        
    else:
        form=BusinessForm()
    return render(request,'add_business.html',{'form':form})    

@login_required(login_url='/login')
def search(request, hood_id):
    current_user=request.user
    hood=Neighbourhood.find_neighbourhood(hood_id)
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        businesses=Business.objects.filter(name__icontains = search_term , neighbourhood=hood)
        message=f'{search_term}'

        return render(request, 'search-page.html', {'message':message, 'businesses':businesses, 'current_user':current_user})

    else:
        message='Enter term to search'
        return render(request, 'hood_details.html',{'amenities':amenities,'hood':hood,'occupants':occupants, 'businesses':businesses,'posts':posts,'form':form, 'message':message})

    