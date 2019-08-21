from django.urls import reverse
from django.contrib.auth.models import user
from django.test import TestCase
from django.core import mail
#test tries to access the password_change view without being logged in.The expected behaviour is to redirect the user to the loh iin page.
class LoginRequiredPasswordChnageTests(TestCase):
	def test_redirection(self):
		url=reverse('password_change')
		login_url=reverse('login')
		response=self.client.get(url)
		self.assertRedirects(response,f'{login_url}?next={url}')

#this test does a basic set up creating a user and making a POST request to the password_change view
class PasswordChangeTestCase(TestCase):
	def  setUp(self,data={}):
		self.user=User.objects.create_user(username='john',email='johndoe@gmail.com',password='old_password')
		self.url=reverse('password_change')
		self.client.login(username='john',password='old_password')
		self.response=self.client.post(self.url,data)

class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
	def setUp(self):
		super().setUp({
			'old_password':'old_password',
			'new_password1':'new_password',
			'new_password2':'new_password',
			})
	def test_redirection(self):
		'''
		A valid form submission should redirect the user
		'''
		self.assertRedirects(self.response,reverse('password_change_done'))

	def test_password_changed(self):
		'''
		refresh the user instance from database to get the new password hash updated by the change password view.
		'''
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('new_password'))

	def test_user_authentication(self):
		'''
		Create a new request to an arbitrary page.
		The resulting response should now have a 'user' to its context, after a successful sign up.
		'''
		response=self.client.get(reverse('home'))
		user=response.context.get('user')
		self.assertTrue(user.is_authenticted)

class InvalidPasswordChangeTests(PasswordChangeTestCase):
	def test_status_code(self):
		'''
		An invalid form submission should return to the same page
		'''
		self.assertEquals(self.response.status_code,200)

	def test_form_errors(self):
		form=self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_didnt_change_password(self):
		'''
		refresh the user instance from the database to make sure we have the latest data.
		'''
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('old_password'))
