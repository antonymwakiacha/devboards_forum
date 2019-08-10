from django.test import TestCase
from django.urls import resolve,reverse
from .views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm
#from django.core.urlresolvers import reverse

class SignUpTests(TestCase):
	def setUp(self):
		url=reverse('signup')
		self.response=self.client.get(url)

	def  test_signup_status_code(self):
		url=reverse('signup')
		response=self.client.get(url)
		self.assertEquals(response,status_code,200)

	def  test_signup_url_resolves_signup_view(self):
		view=resolve('/signup')
		self.assertEquals(view.func,signup)

	def test_csrf(self):
		self.assertContains(self.response,'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertInstance(form,SignUpForm)

	#this test ensures verification of HTML inputs in the forms.html template
	def  test_form_inputs(self):
		'''
		The view must contain five inputs:csrf,username,email,password1,password2
		'''
		self.assertContains(self.response,'<input',5)
		self.assertContains(self.response,'type="text"',1)
		self.assertContains(self.response,'type="email"',1)
	
		self.assertContains(self.response,'type="password"',2)
class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url=reverse('signup')
		data= {
			'username': 'john',
			'password1':'abcdef123456',
			'password2':'abcdef123456'			
		}
		self.response=self.client.post(url,data)
		self.home_url=reverse('home')

	def test_redirection(self):
		'''
		A valid form submission should redirect the user to the home page
		'''
		self.assertRedirects(self.response,self.home_url)

	def  test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		'''
		Create a new request to an arbitary page,
		The resulting response should now have a 'user' to its contect,
		after a successful signup.
		'''
		response=self.client.get(self.home_url)
		user=response.context.get('user')
		self.assertTrue(user.is_authenticated)

class   InvalidSignUpTests(TestCase):
	def   setUp(self):
		  url=reverse('signup')
		  self.response=self.client.post(url,{})

    def   test_signup_status_code(self):
    	'''
    	An invlid form submission should return to the same page
    	'''
    	self.assertEquals(self.response.status_code,200)

    def   test_form_errors(self):
    	form=self.response.context.get('form')
    	self.assertTrue(form.errors)

    def   test_dont_create_user(self):
    	   self.assertFalse(User.objects.exists())