from django.urls import path
from . import views
from .views import ItemSearchView



urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # path('record/<int:pk>', views.user_record, name='record'),
    # path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    # path('add_record/', views.add_record, name='add_record'),
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('rsn/', views.retrieve_street_network, name='rsn'),
    path('sl/', views.GetSearchLocation, name='sl'),
    path('route/', views.routing, name='route'),
    path('search/', ItemSearchView.as_view(), name='item-search'),
    #path('gv/', views.getVenues, name='gv'),
]