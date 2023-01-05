from django.db import models


class FoodChoices(models.TextChoices):
    pizza = 'pizza', 'پیتزا'
    burger = 'burger', 'برگر'
    chicken = 'chicken', 'مرغ'
    qorme_sabzi = 'qorme_sabzi', 'قورمه سبزی'
    sabzipolo_mahi = 'sabzipolo_mahi', 'سبزی‌پلو با ماهی'
    gheime_sibzamini = 'gheime_sibzamini', 'قیمه سیب‌زمینی'
    juje_kabab = 'juje_kabab', 'جوجه کباب'
    kabab_kubide = 'kabab_kubide', 'کباب کوبیده'
