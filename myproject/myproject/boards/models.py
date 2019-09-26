from django.db import models
from django.utils.text import Truncator
# Create your models here.

from django.contrib.auth.models import User
from  markdown import markdown
from django.utils.html import mark_safe

class Board(models.Model):
	name=models.CharField(max_length=30,unique=True)
	description=models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
	subject=models.CharField(max_length=255)
	last_updated=models.DateTimeField(auto_now_add=True)
	board=models.ForeignKey(Board,related_name='topics',on_delete=models.DO_NOTHING)
	starter=models.ForeignKey(User,related_name='topics',on_delete=models.DO_NOTHING)
	views=models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.subject
class Post(models.Model):
	message=models.TextField(max_length=4000)
	topic=models.ForeignKey(Topic,related_name='posts',on_delete=models.DO_NOTHING)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(null=True)
	created_by=models.ForeignKey(User,related_name='posts',on_delete=models.DO_NOTHING)
	updated_by=models.ForeignKey(User,null=True,related_name='+',on_delete=models.DO_NOTHING)

	def __str__(self):
		truncated_message=Truncator(self.message)#Truncator utility class used to truncate strings into an arbitrary string size
		return truncated_message.chars(30)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message,safe_mode='escape'))
	#here we are dealing with user input hence when using the markdown function,we are instructing it to escape the special characters first and then parse the markdwon tags.After that we mark the output string as safe to be used in the template.