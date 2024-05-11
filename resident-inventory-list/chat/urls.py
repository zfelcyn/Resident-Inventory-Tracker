from django.urls import path # imports path funmction from django library
from . import views # imports views from local files, each view functionr returns an http result
from .views import RegisterView, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views

# url patterns are something that django uses to route incomming http requests to the appropritate view
# based on the requests url path. An http request is a message sent by a client to a server,\
# asking for some action to be performed on the server. Each http request includes a method, like  the action type(GET to submit data, PUT to update resoure, and DELETE to remove stuff)
# URL, or uniform resource locator, specifies the path to the resource on the server, headers provide additional info like content type, authetication tokens, ect. Finally theres the body, which contains data sent
# with the request.

# A view in context of django, is a python function that takes an http request as input and returns an http result
# Logic in this can include accessing data from the database, processing or transforming data, or deciding what to send back, like a html page,
# json, xml, redirect, whatever. A VIEW FUNCTION IS THE AIR TRAFFIC CONTROL OF THE BACKEND 
urlpatterns = [
    # matches an empty string representing the root URL of the website, and route those requests to the home function
    # in the views module. The name = 'home' assigns a name to the url, which we can type in the website url
    path('login/',CustomLoginView.as_view(), name='home'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('chat/logout/', CustomLogoutView.as_view(), name='logout'),
   
    path('add_resident/', views.add_resident, name='add_resident'),  # URL for adding a resident
    path('add_item/', views.add_item, name='add_item'),  # URL for adding a resident
    
    path('delete_resident/<int:resident_id>/', views.delete_resident, name='delete_resident'),
    path('export_residents_csv/', views.export_residents_csv, name='export_residents_csv'),


    #path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),  # URL for deleting an item
    
    path('regency/', views.regency, name='regency'),  # URL for regency.html

]