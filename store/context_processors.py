"""
Context processor tùy chỉnh: cho phép truy cập số lượng sản phẩm trong giỏ hàng
ở BẤT KỲ template nào (đặc biệt là base.html - Navbar) mà không cần truyền
thủ công trong mỗi view.
"""
from .cart import Cart


def cart_item_count(request):
    try:
        cart = Cart(request)
        return {'cart_item_count': len(cart)}
    except Exception:
        return {'cart_item_count': 0}
