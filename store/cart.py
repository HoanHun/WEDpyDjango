"""
Giỏ hàng (Cart) được lưu trong Session của Django.
Không cần tạo bảng riêng trong Database - dữ liệu giỏ hàng tồn tại
theo phiên làm việc (session) của từng người dùng cho đến khi họ Đặt hàng (checkout).
"""

from decimal import Decimal
from .models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        """Khởi tạo giỏ hàng từ session hiện tại."""
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # Tạo giỏ hàng rỗng trong session
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Thêm sản phẩm vào giỏ hàng hoặc cập nhật số lượng."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Đánh dấu session đã bị thay đổi để Django lưu lại
        self.session.modified = True

    def remove(self, product):
        """Xóa 1 sản phẩm khỏi giỏ hàng."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Duyệt qua các sản phẩm trong giỏ hàng, lấy thêm object Product từ DB."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Tổng số lượng sản phẩm (cộng dồn quantity) trong giỏ hàng."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Tính tổng tiền của toàn bộ giỏ hàng."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Xóa toàn bộ giỏ hàng khỏi session (gọi sau khi đặt hàng thành công)."""
        del self.session[CART_SESSION_ID]
        self.save()
