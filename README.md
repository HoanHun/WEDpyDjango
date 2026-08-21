<<<<<<< HEAD
# Shop – Trang web bán quần áo (Django)

Dự án Django hoàn chỉnh cho website bán quần áo, đáp ứng đầy đủ yêu cầu:
Models (Product/Category/Order), đăng ký/đăng nhập/đăng xuất, giỏ hàng + đặt hàng,
giao diện Bootstrap 5 responsive với `base.html` dùng chung.

> ⚠️ **Lưu ý quan trọng**: Dự án này được viết để bạn **tự chạy trên máy tính cá nhân
> hoặc host lên một dịch vụ hỗ trợ Python** (Render, Railway, PythonAnywhere, VPS, vân vân).
> Nó **không** chạy được trên Cloudflare Pages/Workers và chưa hỗ trợ các thứ khác ...
> Python, không có filesystem để lưu ảnh upload, và không chạy được Django ORM.

---

## 1. Cấu trúc dự án

```
pywedBanHang/ (bán hàng online)
├── manage.py
├── requirements.txt
├── shop_project/          # Cấu hình chính (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/                  # App chính chứa toàn bộ nghiệp vụ
│   ├── models.py            # Category, Product, Order, OrderItem
│   ├── views.py              # Toàn bộ views (trang chủ, chi tiết SP, auth, giỏ hàng, đặt hàng)
│   ├── urls.py
│   ├── forms.py              # SignUpForm, CheckoutForm
│   ├── admin.py               # Đăng ký models vào trang /admin/
│   ├── cart.py                 # Giỏ hàng lưu trong session
│   ├── context_processors.py   # Hiển thị số lượng giỏ hàng ở Navbar
│   └── fixtures/sample_data.json  # Dữ liệu mẫu (4 danh mục, 10 sản phẩm)
├── templates/
│   ├── base.html                  # Khung chuẩn: Navbar + Footer (Bootstrap 5)
│   ├── registration/
│   │   ├── login.html
│   │   └── signup.html
│   └── store/
│       ├── home.html               # Trang chủ - danh sách sản phẩm
│       ├── product_detail.html     # Chi tiết sản phẩm
│       ├── cart_detail.html        # Giỏ hàng
│       ├── checkout.html           # Đặt hàng
│       ├── order_list.html         # Danh sách đơn hàng của tôi
│       └── order_detail.html       # Chi tiết 1 đơn hàng
├── static/
│   ├── css/style.css
│   └── js/main.js
└── media/                   # Nơi lưu ảnh sản phẩm upload qua trang Admin
```

---

## 2. Cài đặt & Chạy dự án (Local)

### Bước 1: Tạo môi trường ảo (khuyến nghị  )
```bash
cd pywedBanHang
python3 -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
>> lưu ý :
>> Nó giúp tạo ra một vùng làm việc độc lập, chứa phiên bản Python riêng và các thư viện (như Django, Flask, Pillow...) chỉ phục vụ cho dự án đó mà không   >> ảnh hưởng đến máy tính hoặc các dự án khác.
>> tránh xung đột thư viện, gọn nghẹ và dễ chia sẻ cho nhau, giữ sạch hệ điều hành 
### Bước 2: Cài thư viện
```bash
pip install -r requirements.txt
```
(`requirements.txt` gồm `Django` và `Pillow` — Pillow bắt buộc để dùng `ImageField`)

### Bước 3: Tạo database & bảng (migrations)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 4: (Tuỳ chọn) Nạp dữ liệu mẫu — 4 danh mục + 10 sản phẩm
```bash
python manage.py loaddata sample_data.json
```

### Bước 5: Tạo tài khoản quản trị (Admin)
```bash
python manage.py createsuperuser
```
Nhập username, email, password theo hướng dẫn.

### Bước 6: Chạy server phát triển
```bash
python manage.py runserver
```
Mở trình duyệt tại: **http://127.0.0.1:8000/**

Trang quản trị (Admin): **http://127.0.0.1:8000/admin/**
→ Dùng để thêm/sửa Sản phẩm, Danh mục, xem/đổi trạng thái Đơn hàng, upload hình ảnh sản phẩm.
>>> Lưu ý chủ chạy được trên máy bạn chỉ là host nội bộ
---

## 3. Danh sách trang & URL

| URL | Chức năng |
|---|---|
| `/` | Trang chủ – danh sách sản phẩm (lọc theo danh mục `?category=<id>`, tìm kiếm `?q=...`, phân trang `?page=`) |
| `/product/<id>/` | Trang chi tiết sản phẩm |
| `/signup/` | Đăng ký tài khoản |
| `/login/` | Đăng nhập |
| `/logout/` | Đăng xuất |
| `/cart/` | Xem giỏ hàng |
| `/cart/add/<id>/` | Thêm sản phẩm vào giỏ hàng (POST) |
| `/cart/update/<id>/` | Cập nhật số lượng trong giỏ hàng (POST) |
| `/cart/remove/<id>/` | Xóa sản phẩm khỏi giỏ hàng (POST) |
| `/checkout/` | Đặt hàng (yêu cầu đăng nhập) |
| `/orders/` | Danh sách đơn hàng của tôi (yêu cầu đăng nhập) |
| `/orders/<id>/` | Chi tiết 1 đơn hàng (yêu cầu đăng nhập) |
| `/admin/` | Trang quản trị Django mặc định |

---

## 4. Models (Database)

- **`Category`**: `name`, `slug` (tự sinh)
- **`Product`**: `name`, `price`, `image` (ImageField → lưu vào `media/products/`), `description`,
  `category` (FK → Category), `stock`, `created_at`, `updated_at`
- **`Order`**: `user` (FK → User mặc định của Django), `total_amount`, `payment_status`
  (pending/paid/cancelled/shipped/completed), `shipping_address`, `phone_number`, `created_at`
- **`OrderItem`**: chi tiết từng sản phẩm trong 1 đơn hàng — `order`, `product`, `product_name`
  (lưu snapshot tên để tránh mất dữ liệu nếu sản phẩm bị xóa), `price`, `quantity`

**Giỏ hàng (Cart)** không tạo bảng riêng — được lưu trong **Django Session** (file `store/cart.py`),
và chỉ được ghi thành `Order` + `OrderItem` trong DB khi người dùng bấm "Đặt hàng" (checkout).

---

## 5. Cấu hình STATIC & MEDIA (đã setup sẵn trong `settings.py`)

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']       # Nơi để CSS/JS khi phát triển
STATIC_ROOT = BASE_DIR / 'staticfiles'         # Nơi gom file khi chạy collectstatic (production)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'                # Nơi lưu ảnh sản phẩm upload qua Admin
```

Khi `DEBUG=True`, Django tự phục vụ cả static và media qua `urls.py`
(`+ static(...)`). Khi deploy production (`DEBUG=False`), bạn cần:
- Chạy `python manage.py collectstatic` và cấu hình web server (Nginx/Whitenoise) phục vụ `staticfiles/`
- Dùng dịch vụ lưu trữ file bên ngoài (ví dụ AWS S3, Cloudinary) cho `media/` vì hầu hết host
  Python (Render, Railway...) có filesystem tạm thời (ephemeral), ảnh upload sẽ mất khi redeploy.

---

## 6. Đưa lên Production (gợi ý)

1. Đổi `SECRET_KEY` sang biến môi trường, đặt `DEBUG = False`
2. Cập nhật `ALLOWED_HOSTS = ['yourdomain.com']`
3. Đổi Database sang PostgreSQL (khuyến nghị cho production):
   ```python
   DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
   ```
4. Cài `whitenoise` để phục vụ static files, hoặc dùng S3/Cloudinary cho media
5. Deploy lên: **Render.com**, **Railway.app**, **PythonAnywhere**, hoặc VPS + Gunicorn + Nginx

---

## 7. Việc chưa hoàn thiện / hướng phát triển tiếp

- [ ] Tích hợp cổng thanh toán thật (VNPay, Momo, Stripe...) — hiện tại chỉ có trạng thái
      thanh toán demo (COD/pending)
  
- [ ] Trang quản lý đơn hàng riêng cho khách hàng (hủy đơn, theo dõi vận chuyển)
- [ ] Đánh giá & bình luận sản phẩm (Review/Rating)
- [ ] Wishlist (danh sách yêu thích)
- [ ] Bộ lọc nâng cao (theo giá, size, màu sắc)
- [ ] Gửi email xác nhận đơn hàng (Django `send_mail` + SMTP)
- [ ] API REST (Django REST Framework) nếu cần tách frontend riêng (React/Vue)
- [ ] Unit test cho views/models

---

## 8. Công nghệ sử dụng

- **Backend**: Python 3.10+, Django 5.0
- **Database**: SQLite (mặc định, dev) — khuyến nghị PostgreSQL cho production (nhưng bị lỗi khi up nên chưa cài vào postgreSQL)
- **Frontend**: Bootstrap 5.3 (CDN), Font Awesome 6 (CDN), CSS/JS tùy chỉnh
- **Ảnh sản phẩm**: Pillow + Django `ImageField` + `MEDIA_ROOT`
=======
# WEDpyDjango
>>>>>>> 6d153f2fb0e31eaf000319517f6ad1d68a348f71
