"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^db/', views.db),

    ##########################################################################
    ######################	ADMIN PANEL URL  #################################
    ##########################################################################

    #***** LOGIN FOR ADMIN ******
    url(r'^dashboard/', views.login),
    
    #***** LOGOUT FOR ADMIN *****
    url(r'^logout/', views.logout),

    #***** VIEW COMMENTS FOR ADMIN *****
    url(r'^view_users/', views.view_users),

    #***** CRUD AT CATEGORY *****
    url(r'^add_category/', views.add_category),
    url(r'^view_category/', views.view_category),
    url(r'^delete_category/(?P<id>\d+)/$', views.delete_category),
    url(r'^edit_category/(?P<id>\d+)/$', views.edit_category),

    #***** CRUD AT POST *****
    url(r'^add_news/', views.add_news),
    url(r'^view_news/', views.view_news),
    url(r'^delete_news/(?P<id>\d+)/$', views.delete_news),
    url(r'^edit_news/(?P<id>\d+)/$', views.edit_news),

    

    ##########################################################################
    ######################	FRONT-END URL  ###################################
    ##########################################################################

    #***** INDEX PAGE *****
    url(r'^$', views.index),

    #***** BLOG PAGE *****
    url(r'^news/', views.news),

    #***** BLOG PAGE *****
    url(r'^contact/', views.contact),

    #***** ABOUT US PAGE *****
    url(r'^about/', views.about),

    #***** BLOG DETAIL PAGE *****
    url(r'^newsdetail/(?P<id>\d+)/$', views.newsdetail),

    #***** POST AGAINST CATEGORY PAGE *****
    url(r'^catnews/(?P<id>\d+)/$', views.catnews),

    #***** POST AGAINST CATEGORY PAGE *****
    url(r'^signup/', views.signup),

    #***** LOGIN PAGE *****
    url(r'^login/', views.userlogin),

    #***** LOGOUT PAGE *****
    url(r'^userlogout/', views.userlogout),

    #***** BOOKMARK NEW NEWS PAGE *****
    url(r'^add_bookmarknews/(?P<id>\d+)/$', views.add_bookmarknews),

    #***** BOOKMARK NEWS PAGE *****
    url(r'^bookmarknews/', views.bookmarknews),

]
