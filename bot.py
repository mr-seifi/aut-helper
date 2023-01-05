#!/usr/bin/env python

import os
import logging
from uuid import uuid4
from telegram import __version__ as TG_VER
from core.models import Student
from core.services import CoreCacheService
from django.conf import settings
from dotenv import load_dotenv
from _helpers import weekday_to_persian_weekday, weekday_to_date_from_now, split, NotEnoughBalance
from easy_food.services import FoodUpdaterService, FoodCacheService, FoodReservationService
from easy_book.services import BookService, OnlineBookService
from easy_book.models import LibraryBook, OnlineBook
from payment.services import PaymentService
from payment.enums import TransactionChoices

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
)

from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about university."""
    message = update.message
    user_id = message.from_user.id

    is_registered = False
    if Student.objects.filter(student_id=user_id).exists():
        is_registered = True

    if not is_registered:
        return await register(update, context)

    return await menu(update, context)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a user with his/her name."""
    message = update.message
    user_id = message.from_user.id

    await message.reply_text(
        settings.MESSAGES['register_name'],
    )

    return settings.STATES['register_1']


async def _register(update: Update, _: ContextTypes.DEFAULT_TYPE, field: str, message_field: str, next_state: int):
    message = update.message
    user_id = message.from_user.id

    cache_service = CoreCacheService()
    getattr(cache_service, f'cache_{field}')(student_id=user_id,
                                             **{field: message.text})
    await message.reply_text(
        settings.MESSAGES[f'register_{message_field}'],
    )

    return settings.STATES[f'register_{next_state}']


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a user with his/her ."""
    return await _register(update, context, 'name', 'enter_year', 2)


async def register_enter_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a user with his/her ."""
    return await _register(update, context, 'enter_year', 'number', 3)


async def register_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    user_id = message.from_user.id

    cache_service = CoreCacheService()
    params = {'name': cache_service.get_name(student_id=user_id),
              'enter_year': cache_service.get_enter_year(student_id=user_id),
              'phone_number': message.text,
              'student_id': user_id}
    if not params['name'] or not params['enter_year']:
        await message.reply_text(
            settings.MESSAGES['expired']
        )

        return ConversationHandler.END

    Student.objects.create(**params)
    await message.reply_text(
        settings.MESSAGES['register_done']
    )

    return ConversationHandler.END


async def menu(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message
    query = None
    if not message:
        query = update.callback_query
        user_id = query.from_user.id
    else:
        user_id = message.from_user.id

    keyboard = [
        [
            InlineKeyboardButton('بوک‌بنک', callback_data=2),
            InlineKeyboardButton('کتابخانه', callback_data=1),
        ],
        [
            InlineKeyboardButton('رزرو غذا', callback_data=0),
            InlineKeyboardButton('کیف پول', callback_data=4)
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if message:
        await message.reply_text(
            settings.MESSAGES['menu'],
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        try:
            await query.edit_message_text(
                settings.MESSAGES['menu'],
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            await query.message.reply_text(
                settings.MESSAGES['menu'],
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )

    return settings.STATES['menu']


async def food_reserve(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    food_updater_service = FoodUpdaterService()
    food_reservation_service = FoodReservationService()
    _reserved_weekdays = food_reservation_service.get_weekday_student_cycle_reserved_foods(student_id=user_id)

    food_cycle = '\n'.join([(settings.MESSAGES['menu_food_item'].format(day=weekday_to_persian_weekday(weekday),
                                                                        food=food),
                             settings.MESSAGES['menu_food_item_reserved'].format(
                                 day=weekday_to_persian_weekday(weekday),
                                 food=food))[weekday in _reserved_weekdays]
                            for weekday, food in food_updater_service.get_a_food_cycle().items()])
    keyboard = split([
        InlineKeyboardButton(weekday_to_persian_weekday(weekday), callback_data=weekday)
        for weekday in food_updater_service.get_a_food_cycle().keys() if weekday not in _reserved_weekdays
    ], 4)
    keyboard += [
        [
            InlineKeyboardButton('منوی اصلی', callback_data=-1)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"{settings.MESSAGES['menu_food_main']}\n"
        f"{food_cycle}",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    return settings.STATES['food']


async def food_reserve_confirm(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    food_updater_service = FoodUpdaterService()
    food_cache_service = FoodCacheService()
    food = food_updater_service.get_a_food_cycle()[int(query.data)]
    food_price = food_cache_service.get_food_price(food=food)

    keyboard = [
        [
            InlineKeyboardButton('آره', callback_data=f'1:{int(query.data)}')
        ],
        [
            InlineKeyboardButton('نه', callback_data=f'0:{int(query.data)}')
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.answer()

    await query.edit_message_text(
        settings.MESSAGES['menu_food_reserve_confirm'].format(
            food=food,
            price=food_price,
            day=weekday_to_persian_weekday(int(query.data))
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return settings.STATES['food']


async def food_reserve_done(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    if '0:' in query.data:
        return await menu(update, _)

    food_updater_service = FoodUpdaterService()
    food_reservation_service = FoodReservationService()
    _week_day = int(query.data.split(':')[-1])
    _reservation_date = weekday_to_date_from_now(_week_day)
    food = food_updater_service.get_a_food_cycle()[_week_day]
    await query.answer()

    try:
        food_reservation_service.reserve_food(student_id=user_id,
                                              food=food,
                                              reserve_date=_reservation_date)
    except NotEnoughBalance:
        await query.edit_message_text(
            settings.MESSAGES['not_enough_balance']
        )

        return ConversationHandler.END

    await query.edit_message_text(
        settings.MESSAGES['menu_food_reserve_done']
    )

    return ConversationHandler.END


async def wallet(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    balance = Student.objects.filter(student_id__exact=user_id).first().balance
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton('افزایش موجودی', callback_data=0)
        ],
        [
            InlineKeyboardButton('تراکنش‌ها', callback_data=1)
        ],
        [
            InlineKeyboardButton('منوی اصلی', callback_data=-1)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        settings.MESSAGES['wallet'].format(balance=balance),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

    return settings.STATES['wallet']


async def wallet_deposit(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('20,000 تومان', callback_data=20000)
        ],
        [
            InlineKeyboardButton('50,000 تومان', callback_data=50000)
        ],
        [
            InlineKeyboardButton('100,000 تومان', callback_data=100000)
        ],
        [
            InlineKeyboardButton('منوی اصلی', callback_data=-1)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        settings.MESSAGES['wallet_deposit'],
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

    return settings.STATES['wallet']


async def wallet_deposit_done(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    balance = int(query.data)

    payment_service = PaymentService()
    payment_service.make_transaction(price=balance,
                                     student_id=user_id,
                                     transaction_type=TransactionChoices.DEPOSIT)

    await query.edit_message_text(
        settings.MESSAGES['wallet_deposit_done'],
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


async def transaction_history(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    payment_service = PaymentService()
    transactions = payment_service.get_student_transactions(student_id=user_id)

    transactions_message = '\n'.join(map(lambda t: str(t), transactions))
    await query.edit_message_text(
        f"{settings.MESSAGES['transactions_history']}\n\n"
        f"{transactions_message}",
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


async def bookbank_reference(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('جستجوی کتاب', switch_inline_query_current_chat='')
        ],
        [
            InlineKeyboardButton('منوی اصلی', callback_data=-1)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_photo(
        photo='asset/book-bank.jpg',
        caption=settings.MESSAGES['bookbank_reference'],
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

    return settings.STATES['menu']


async def library(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('جستجوی کتاب', switch_inline_query_current_chat='library')
        ],
        [
            InlineKeyboardButton('منوی اصلی', callback_data=-1)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_photo(
        photo='asset/aut-helper.jpg',
        caption=settings.MESSAGES['library'],
        reply_markup=markup
    )

    return settings.STATES['menu']


async def _search_result(query):
    book_service = BookService()
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=book.title,
            input_message_content=InputTextMessageContent(f'/lookup {book.uid}'),
            thumb_url=f'http://{os.getenv("DOMAIN")}/cover/{book.cover.url.split("?")[0].split("/")[-1].split("_")[0]}.'
                      f'{book.cover.url.split("?")[0].split("/")[-1].split(".")[-1]}'
            if book.cover else '',
            description=f'{book.year + "-" if book.year else ""}'
                        f'{book.authors}\n{book.publisher}'
        ) for book in book_service.search_book(query)
    ]

    return results


async def library_search(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    user_id = update.inline_query.from_user.id

    if query == "":
        return

    book_service = BookService()
    results = await _search_result(query)
    for book in book_service.search_book(query):
        logger.info(book.cover.url.replace(f"{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}",
                                           os.getenv('DOMAIN')).split('?')[0]
                    if book.cover else '')

    response = await update.inline_query.answer(results)
    return response


async def bookbank_search(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    user = update.inline_query.from_user

    if query == "":
        return

    if 'library' in query:
        query = query.replace('library', '')
        results = await _search_result(query)

        response = await update.inline_query.answer(results)
        return response

    book_service = OnlineBookService()
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=book.title,
            input_message_content=InputTextMessageContent(f'/download {book.md5}'),
            thumb_url=book.cover_url,
            description=f'{book.year + "-" if book.year else ""}{book.extension + "-" if book.extension else ""}'
                        f'{(book.filesize // 1000000) + 1}MB\n'
                        f'{book.authors}\n{book.publisher}\n{book.description}'
        ) for book in book_service.search_book(query)
    ]
    response = await update.inline_query.answer(results)
    return response


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    try:
        uid = context.args[0]
    except IndexError:
        return
    except TypeError:
        return
    except Exception:
        return

    book = LibraryBook.objects.filter(uid__exact=uid).first()
    if book.cover:
        try:
            await message.reply_photo(
                photo=f'http://{os.getenv("DOMAIN")}/cover/{book.cover.url.split("?")[0].split("/")[-1]}',
                caption=settings.MESSAGES['book'].format(title=book.title,
                                                         status=('ناموجود', 'موجود')[book.is_exist]),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            await message.reply_text(
                settings.MESSAGES['book'].format(title=book.title,
                                                 status=('ناموجود', 'موجود')[book.is_exist]),
                parse_mode=ParseMode.MARKDOWN
            )
        return

    await message.reply_text(
        settings.MESSAGES['book'].format(title=book.title,
                                         status=('ناموجود', 'موجود')[book.is_exist]),
        parse_mode=ParseMode.MARKDOWN
    )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    try:
        md5 = context.args[0]
    except IndexError:
        return
    except TypeError:
        return

    try:
        book = OnlineBook.objects.get(md5=md5)
    except OnlineBook.DoesNotExist:
        return

    message_id = book.file
    response = await context.bot.forward_message(chat_id=user_id,
                                                 from_chat_id='-1001590420573',
                                                 message_id=message_id)
    return response


def main() -> None:
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            settings.STATES['register']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register)
            ],
            settings.STATES['register_1']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)
            ],
            settings.STATES['register_2']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_enter_year)
            ],
            settings.STATES['register_3']: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_number)
            ],
            settings.STATES['menu']: [
                CallbackQueryHandler(menu, pattern=r'^-1$'),
                CallbackQueryHandler(food_reserve, pattern=r'^0$'),
                CallbackQueryHandler(library, pattern=r'^1$'),
                CallbackQueryHandler(bookbank_reference, pattern=r'^2$'),
                CallbackQueryHandler(wallet, pattern=r'^4$'),
            ],
            settings.STATES['food']: [
                CallbackQueryHandler(menu, pattern=r'^-1$'),
                CallbackQueryHandler(food_reserve_confirm, pattern=r'^[0-6]$'),
                CallbackQueryHandler(food_reserve_done, pattern=r'^(0|1)\:[0-9]$'),
            ],
            settings.STATES['wallet']: [
                CallbackQueryHandler(menu, pattern=r'^-1$'),
                CallbackQueryHandler(wallet_deposit, pattern=r'^0$'),
                CallbackQueryHandler(transaction_history, pattern=r'^1$'),
                CallbackQueryHandler(wallet_deposit_done, pattern=r'^(?:20000|50000|100000)$'),
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    ))
    application.add_handler(
        CommandHandler('lookup', lookup)
    )
    application.add_handler(
        CommandHandler('download', download)
    )
    application.add_handler(
        InlineQueryHandler(bookbank_search)
    )
    application.run_polling()
