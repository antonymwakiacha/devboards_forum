from django.shortcuts import redirect,render,get_object_or_404
# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required



def home(request):
	boards=Board.objects.all()
	return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
	board=get_object_or_404(Board,pk=pk)
	return render(request,'topics.html',{'board':board})


#django decorator to avoid non-logged in user from accessing the new_topic page
@login_required#if the user is not authenticated they will be redirected to the log in page
def  new_topic(request,pk):
	board=get_object_or_404(Board,pk=pk)
	#user=User.objects.first()

	if request.method=='POST':
		form=NewTopicForm(request.POST)#initiating a form instance
		if form.is_valid():#django checks the validity of the form 
			topic=form.save(commit=False)#saves data in the database
			#save()#returns an instance of the model saved imto the database
			topic.board=board
			topic.starter=request.user
			topic.save()
			Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=request.user
				)
			return redirect('board_topics',pk=board.pk)#TODO:redirect to the created topic page
	else:
			form=NewTopicForm()#initializes an empty form if the request was a GET
	return render(request,'new_topic.html',{'board':board,'form':form})

def topic_posts(request,pk,topic_pk):
	topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
	return render(request,'topic_posts.html',{'topic':topic})
	# 	subject=request.POST['subject']
	# 	message=request.POST['message']

	# 	user=User.objects.first()#TODO:get the currently logged in user

	# 	topic=Topic.objects.create(
	# 		subject=subject,
	# 		board=board,
	# 		starter=user
	# 		)

	# 	post=Post.objects.create(
	# 		message=message,
	# 		topic=topic,
	# 		created_by=user
	# 		)

	# 	return redirect('board_topics',pk=board.pk)#TODO:redirect to the created topic page

	# return render(request,'new_topic.html',{'board':board})


	# return render(request,'new_topic.html',{'board':board})
	# # boards=Board.objects.all()
	# # boards_names=list()

	# # for board in boards:
	# # 	boards_names.append(board.name)

	# # 	response_html='<br>'.join(boards_names)


	# # return HttpResponse(response_html) 

