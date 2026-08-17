from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Bảng Danh mục (Category): Tên danh mục."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên danh mục')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Tự động tạo slug từ tên danh mục nếu chưa có
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Bảng Sản phẩm (Product): Tên, Giá, Hình ảnh, Mô tả, Danh mục."""
    name = models.CharField(max_length=255, verbose_name='Tên sản phẩm')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Giá (VNĐ)')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Hình ảnh')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Danh mục'
    )
    stock = models.PositiveIntegerField(default=100, verbose_name='Số lượng tồn kho')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class Order(models.Model):
    """Bảng Đơn hàng (Order): Liên kết với User, Tổng tiền, Trạng thái thanh toán."""

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Chờ thanh toán'
        PAID = 'paid', 'Đã thanh toán'
        CANCELLED = 'cancelled', 'Đã hủy'
        SHIPPED = 'shipped', 'Đang giao hàng'
        COMPLETED = 'completed', 'Hoàn thành'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Người đặt hàng'
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Tổng tiền (VNĐ)')
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='Trạng thái thanh toán'
    )
    shipping_address = models.CharField(max_length=255, blank=True, verbose_name='Địa chỉ giao hàng')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Số điện thoại')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đặt')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return f'Đơn hàng #{self.pk} - {self.user.username}'


class OrderItem(models.Model):
    """Chi tiết từng sản phẩm trong một đơn hàng (bảng phụ trợ cho Order)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)  # Lưu lại tên phòng khi sản phẩm bị xóa
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Đơn giá lúc mua')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    def get_total(self):
        return self.price * self.quantity
