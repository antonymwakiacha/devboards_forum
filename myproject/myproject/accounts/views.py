from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import	SignUpForm

def signup(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():#validates the form
			user=form.save()#User instance created
			auth_login(request,user)#created user is passed as a parameter to manually authenticate the user
			return redirect('home')#redirects to homepage
	else:
		form=SignUpForm()
	return render(request,'signup.html',{'form':form})

