from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('cart',views.cart,name='cart'),
    path('cart_page/',views.cart_page,name='cart_page'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('collections',views.collections,name='collections'),
    path('fav',views.fav,name='fav'),
    path('fav_page',views.fav_page,name='fav_page'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('remove_fav/<str:fid>',views.remove_fav,name='remove_fav'),
    path('collections/<str:name>',views.collectionsview,name='collections'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='product_details'),
]