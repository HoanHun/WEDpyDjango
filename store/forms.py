from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order


class SignUpForm(UserCreationForm):
    """Form Đăng ký tài khoản - mở rộng từ UserCreationForm mặc định của Django,
    thêm trường email."""
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class Bootstrap cho tất cả các trường
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class CheckoutForm(forms.ModelForm):
    """Form nhập thông tin giao hàng khi Đặt hàng (checkout)."""

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']
        labels = {
            'shipping_address': 'Địa chỉ giao hàng',
            'phone_number': 'Số điện thoại',
        }
        widgets = {
            'shipping_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09xxxxxxxx'
            }),
        }
