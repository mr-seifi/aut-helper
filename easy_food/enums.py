from django.db import models


class FoodChoices(models.TextChoices):
    pizza = 'pizza', 'پیتزا'
    burger = 'burger', 'برگر'
    chicken = 'chicken', 'مرغ'
    qorme_sabzi = 'qorme_sabzi', 'قورمه سبزی'
    sabzipolo_mahi = 'sabzipolo_mahi', 'سبزی‌پلو با ماهی'
    gheime_sibzamini = 'gheime_sibzamini', 'قیمه سیب‌زمینی'
    juje_kabab = 'gheime_sibzamini', 'جوجه کباب'
    kabab_kubide = 'gheime_sibzamini', 'کباب کوبیده'
