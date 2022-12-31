
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))

# Server's ip
SERVER_IP = os.getenv('SERVER_IP')

ALLOWED_HOSTS = [SERVER_IP]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'core',
    'easy_food',
    'easy_book',
    'payment',
    'monitoring',
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

ROOT_URLCONF = 'aut_helper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aut_helper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}
REDIS_DEFAULT_EX = 60 * 5
REDIS_REGISTER_EX = REDIS_DEFAULT_EX
REDIS_FOOD_EX = 60 * 60 * 7

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = os.getenv('RABBITMQ_HOST')

# Minio
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")

AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False

# Payments
MINIMUM_STUDENT_BALANCE = -25000

# Library
LIBRARY_URL = os.getenv('LIBRARY_URL')

# Telegram messages
MESSAGES = {
    'register_name': 'سلام، به من خوش اومدی، لطفا اسمتو بهم بگو تا بدونم.',
    'register_enter_year': 'ورودی چه سالی هستی؟ لطفا به صورت کامل بنویس یعنی اینطوری 1399',
    'register_number': 'لطفا شماره موبایلتو وارد کن.',
    'register_expired': 'لطفا دوباره تلاش کنید.',
    'register_done': 'ثبت‌نام با موفقیت انجام شد. \U00002705',
    'menu': '*منو*\n\n'
            'از بین گزینه‌های زیر، گزینه‌ای رو که می‌خوای انتخاب کن.',
    'menu_food_main': 'منوی غذای این هفته\n',
    'menu_food_item': '{day}: *{food}*',
    'menu_food_item_reserved': '{day}: *{food}* (**رزرو شده**)',
    'menu_food_reserve_confirm': 'آیا مطمئنی می‌خوای *{food}* رو با قیمت *{price}* تومان برای روز *{day}* رزرو کنی؟',
    'menu_food_reserve_done': 'غذا با موفقیت رزرو شد.',
    'not_enough_balance': 'موجودی کافی نیست.',
    'wallet': 'موجودی شما: *{balance}* تومان',
    'wallet_deposit': 'مبلغی که می‌خواهید به ولت خود اضافه کنید را انتخاب کنید.',
    'wallet_deposit_done': 'عملیات با موفقیت انجام شد.',
    'transactions_history': 'تراکنش‌های شما',
    'bookbank_reference': 'برای اینکه بتونی بین کتابام سرچ کنی روی *جستجوی کتاب*'
                          ' کلیک کن. **یادت بمونه که کتاب فارسی نداریم**.',
    'library': 'برای اینکه بتونی بین کتابای کتابخونه سرچ کنی روی جستجوی کتاب کلیک کن.',
    'book': 'کتاب {title} *{status}* می‌باشد. برای دریافت به کتابخانه‌ی دانشکده ریاضی مراجعه کنید.'
}

# Telegram states
STATES = {
    'register': 0,
    'register_1': 1,
    'register_2': 2,
    'register_3': 3,
    'menu': 4,
    'food': 5,
    'wallet': 6,
    'library': 7,
}



