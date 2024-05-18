from django.urls import path
from .views import ProductListView,ProductGetView,CartAPI,OrderCreateView,UserRegistrationView,LoginView


urlpatterns=[
    path('product-list',ProductListView.as_view(),name='product_list'),
    path('product-detail/<int:id>',ProductGetView.as_view(),name='product_detail'),
    path('order-create',OrderCreateView.as_view(),name='order_create'),
    path('cart', CartAPI.as_view(), name='cart'),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name='login')
]