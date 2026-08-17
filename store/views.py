from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Product, Category, Order, OrderItem
from .forms import SignUpForm, CheckoutForm
from .cart import Cart


# ---------------------------------------------------------------------------
# TRANG CHỦ - Hiển thị danh sách sản phẩm (có lọc theo danh mục + tìm kiếm)
# ---------------------------------------------------------------------------
def home(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Lọc theo danh mục nếu có query string ?category=<id>
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Tìm kiếm theo tên sản phẩm nếu có query string ?q=...
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Phân trang: 8 sản phẩm mỗi trang
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'query': query or '',
    }
    return render(request, 'store/home.html', context)


# ---------------------------------------------------------------------------
# TRANG CHI TIẾT SẢN PHẨM
# ---------------------------------------------------------------------------
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


# ---------------------------------------------------------------------------
# ĐĂNG KÝ TÀI KHOẢN
# ---------------------------------------------------------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}! Tài khoản đã được tạo thành công.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# ---------------------------------------------------------------------------
# ĐĂNG NHẬP
# ---------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Xin chào {user.username}, bạn đã đăng nhập thành công!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'registration/login.html')


# ---------------------------------------------------------------------------
# ĐĂNG XUẤT
# ---------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('home')


# ---------------------------------------------------------------------------
# GIỎ HÀNG - Thêm sản phẩm vào giỏ hàng
# ---------------------------------------------------------------------------
@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng.')

    next_url = request.POST.get('next') or 'cart_detail'
    return redirect(next_url)


# ---------------------------------------------------------------------------
# GIỎ HÀNG - Xóa sản phẩm khỏi giỏ hàng
# ---------------------------------------------------------------------------
@require_POST
def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    messages.info(request, f'Đã xóa "{product.name}" khỏi giỏ hàng.')
    return redirect('cart_detail')


# ---------------------------------------------------------------------------
# GIỎ HÀNG - Cập nhật số lượng
# ---------------------------------------------------------------------------
@require_POST
def cart_update(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    else:
        cart.remove(product)
    return redirect('cart_detail')


# ---------------------------------------------------------------------------
# GIỎ HÀNG - Xem chi tiết giỏ hàng
# ---------------------------------------------------------------------------
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})


# ---------------------------------------------------------------------------
# ĐẶT HÀNG (Checkout) - Yêu cầu đăng nhập
# ---------------------------------------------------------------------------
@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống. Vui lòng chọn sản phẩm trước khi đặt hàng.')
        return redirect('home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = cart.get_total_price()
                order.payment_status = Order.PaymentStatus.PENDING
                order.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        price=item['price'],
                        quantity=item['quantity'],
                    )

                cart.clear()
            messages.success(request, f'Đặt hàng thành công! Mã đơn hàng của bạn là #{order.pk}.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


# ---------------------------------------------------------------------------
# XEM DANH SÁCH ĐƠN HÀNG CỦA TÔI
# ---------------------------------------------------------------------------
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/order_list.html', {'orders': orders})


# ---------------------------------------------------------------------------
# XEM CHI TIẾT 1 ĐƠN HÀNG
# ---------------------------------------------------------------------------
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
