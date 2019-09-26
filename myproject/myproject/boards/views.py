from django.db.models import Count
from django.shortcuts import redirect,render,get_object_or_404

from django.contrib.auth.models import User
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostForm
from django.utils import timezone
from django.views.generic import UpdateView,ListView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *

class BoardListView(ListView):
	model=Board
	context_object_name='boards'
	template_name='home.html'

# def home(request):
# 	boards=Board.objects.all()
# 	return render(request,'home.html',{'boards':boards})

# class TopicListView(ListView):
# 	model=Topic
# 	context_object_name='topics'
# 	tempalate_name='topics.html'
# 	paginate_by=20
# 	#board=get_object_or_404(Board,pk=pk)

# 	def get_context_data (self,**kwargs):
# 		super(board,self)._init__(*args,**kwargs)
# 		kwargs['board']=self.board
# 		return super().get_context_data(**kwargs)

# 	def get_query_set(self):
# 		self.board=get_object_or_404(Board,pk=self.kwargs.get('pk'))
# 		queryset=self.board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
# 		return queryset

def board_topics(request,pk):
	board=get_object_or_404(Board,pk=pk)
	queryset=board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
	#topics=board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
	page=request.GET.get('page',1)

	paginator=Paginator(queryset,20)

	try:
		topics=paginator.page(page)
	except PageNotAnInteger:
		#fallback to the first page
		topics=paginator.page(1)
	except EmptyPage:
		#probably the user tried to add a page number
		#in the url,so we fallback to the last page
		topics=paginator.page(paginator.num_pages)

	return render(request,'topics.html',{'board':board,'topics':topics})


#django decorator to avoid non-logged in user from accessing the new_topic page
@login_required#if the user is not authenticated they will be redirected to the log in page
def new_topic(request,pk):
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
			return redirect('topic_posts',pk=pk,topic_pk=topic.pk)#here the topic.pk refers to the object of the Topic model instance thus accessing the pk property
	else:
			form=NewTopicForm()#initializes an empty form if the request was a GET
	return render(request,'new_topic.html',{'board':board,'form':form})

def topic_posts(request,pk,topic_pk):
	topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
	topic.views+=1
	topic.save()
	return render(request,'topic_posts.html',{'topic':topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required,name='dispatch')

class  PostUpdateView(UpdateView):
	model=Post
	fields=('message',)
	template_name='edit_post.html'
	pk_url_kwarg='post_pk'
	context_object_name='post'

	#solution to other users editing any posts problem.
	def get_queryset(self):
		queryset=super().get_queryset()#we are reusing the method from the parent class i.e UpdateView class.Then we are adding an extra filter to the queryset,which is filtering the post using the logged in user,available inside the request object.
		return queryset.filter(created_by=self.request.user)

	def form_valid(self,form):
		post=form.save(commit=False)
		post.updated_by=self.request.user
		post.updated_at=timezone.now()
		post.save()
		return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)

class PostListView(ListView):
	model=Post
	context_object_name='posts'
	template_name='topic_posts.html'
	paginate_by=2

	def get_context_data(self,**kwargs):
		self.topic.views +=1
		self.topic.save()
		kwargs['topic']=self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.topic=get_object_or_404(Topic,board__pk=self.kwargs.get('pk'),pk=self.kwargs.get('topic_pk'))
		queryset=self.topic.posts.order_by('created_at')
		return queryset
# @login_required
# def reply_topic(request,pk,topic_pk):
# 	topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
# 	if request.method == 'POST':
# 		form=PostForm(request.POST)
# 		if form.is_valid():
# 			post=form.save(commit=False)
# 			post.topic=topic
# 			post.created_by=request.user
# 			post.save()
# 			return redirect('topic_posts',pk=pk,topic_pk=topic_pk)#here the topic_pk refers to the keyword of thr function's argument 
# 	else:
# 			form=PostForm()
# 	return render(request,'reply_topic.html',{'topic':topic,'form':form})


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

