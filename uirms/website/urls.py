from django.urls import path, re_path
from . import views
from .views import LocationSearchView



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
    path('gsl/', views.GoToLocation, name='gsl'),
    # path('sla/<float:latitude>/<float:longitude>/<str:name>/', views.GetSearchLocationA, name='sla'),
    # re_path(r'^sla/(?P<latitude>[-]?\d*\.\d+)/(?P<longitude>[-]?\d*\.\d+)/(?P<name>[\w\s.-]+)/$', views.GetSearchLocationA, name='sla'),
    path('route/', views.routing, name='route'),
    path('rec-route/', views.recrouting, name='rec-route'),
    path('search/', LocationSearchView.as_view(), name='location-search'),
    path('recommend-locations/', views.recommend_locations, name='recommend-locations')
]