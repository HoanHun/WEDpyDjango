from django.urls import path
from . import views

urlpatterns = [
    # Trang chủ - danh sách sản phẩm
    path('', views.home, name='home'),

    # Chi tiết sản phẩm
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Đăng ký / Đăng nhập / Đăng xuất
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Giỏ hàng
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/', views.cart_update, name='cart_update'),

    # Đặt hàng & Đơn hàng
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
