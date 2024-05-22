from django.urls import path
from .views import ProductListView,ProductGetView,CartAPI,OrderCreateView,UserRegistrationView,LoginView,CategoryListView,ProductListByCategoryView



urlpatterns=[
    path('product-list',ProductListView.as_view(),name='product_list'),
    path('product-detail/<int:id>',ProductGetView.as_view(),name='product_detail'),
    path('order-create',OrderCreateView.as_view(),name='order_create'),
    path('cart', CartAPI.as_view(), name='cart'),
    path('category-list',CategoryListView.as_view(),name='category_list'),
    path('product-by-category/<int:id>',ProductListByCategoryView.as_view(),name='product_by_category'),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name='login')
]