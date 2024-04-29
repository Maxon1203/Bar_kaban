from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('mapBars', bar_list, name='bar_map'),
    path('bars/reating/', TopBarListView.as_view(), name='bars_reating'),
    path('bars/detail/<int:pk>/', DetailBar.as_view(), name='bar_detail'),
    path('bars/', ListBars.as_view(), name='list_bar'),
    path('bar/fest/', ListFest.as_view(), name='bar_fest'),


    path('profile/<int:pk>/', ProfileUser, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('registr/', user_registration, name='regis_form'),
    path('auth/', user_login, name='auth_form'),
    path('logout/', log_out, name='log out'),
    path('add_comment/<int:review_id>/', add_comment, name='add_comment'),
    path('add_to_favorites/<int:bar_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:bar_id>/', delete_to_favorites, name='delete_to_favorites'),
]