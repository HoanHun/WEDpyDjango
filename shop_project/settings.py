"""
Django settings for shop_project (Trang web bán quần áo).
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------
# SECURITY WARNING: giữ bí mật secret key khi lên production!
# Nên chuyển sang biến môi trường (os.environ) khi deploy thật.
# -----------------------------------------------------------------------
SECRET_KEY = 'django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOY-abcdefgh123456'

# SECURITY WARNING: đặt False khi deploy production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Khi deploy thật, thay bằng domain cụ thể, ví dụ: ['yourdomain.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App của chúng ta
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Thư mục templates dùng chung ở gốc project (base.html, registration/...)
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Context processor tùy chỉnh để hiển thị số lượng giỏ hàng trên Navbar
                'store.context_processors.cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# Mặc định dùng SQLite cho đơn giản. Khi deploy production nên đổi sang PostgreSQL/MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------
# STATIC FILES (CSS, JavaScript)
# -----------------------------------------------------------------------
STATIC_URL = 'static/'
# Thư mục chứa file static khi phát triển (development)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Thư mục Django sẽ gom static files vào khi chạy `collectstatic` (production)
STATIC_ROOT = BASE_DIR / 'staticfiles'


# -----------------------------------------------------------------------
# MEDIA FILES (Hình ảnh do người dùng/admin upload - ví dụ hình sản phẩm)
# -----------------------------------------------------------------------
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------------------------------
# Cấu hình đăng nhập / đăng xuất mặc định của Django
# -----------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
