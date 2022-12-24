from django.utils import timezone


def weekday_to_persian_weekday(w: int):
    return {
        0: 'دوشنبه',
        1: 'سه‌شنبه',
        2: 'چهارشنبه',
        3: 'پنجشنبه',
        4: 'جمعه',
        5: 'شنبه',
        6: 'یکشنبه',
    }[w]


def weekday_to_date_from_now(weekday: int):
    _today_week_day = timezone.now().date().weekday()
    _from_now = ((_today_week_day + weekday) % 7) - 1
    if _from_now < 0:
        _from_now = 6
    return timezone.now().date() + timezone.timedelta(days=_from_now)