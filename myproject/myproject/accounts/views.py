from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import	SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

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

@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
	model=User
	fields=('first_name','last_name','email')
	template_name='my_account.html'
	success_url=reverse_lazy('my_account')

	def get_object(self):
		return self.request.user