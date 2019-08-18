"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include,re_path


from django.contrib.auth import views as auth_views#imported as auth_views to avoid clashing with the boards.view

from accounts import views as accounts_views
from boards import views
urlpatterns = [
    #path('',views.home,name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^signup/$',accounts_views.signup,name='signup'),
    url(r'^login/$',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),#LogooutView.as_view() is a django's class view
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
   # re_path(r'^boards/(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    #path('board/new',views.new_topic,name='new_topic'),
    #url(r'^boards/(?P<pk>\d+)/new/$',views.new_topic,name='new_topic'),
    #path('admin/', admin.site.urls),
     url(r'^admin/', admin.site.urls),
     url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
            ),
        name='password_reset'),
     url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
     url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
]
