#!/usr/bin/env python

import os
import logging
from telegram import __version__ as TG_VER
from core.models import Student
from core.services import CoreCacheService
from django.conf import settings
from dotenv import load_dotenv
from _helpers import weekday_to_persian_weekday
from easy_food.services import FoodUpdaterService

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
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
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
    user_id = message.from_user.id

    keyboard = [
        [
            InlineKeyboardButton('رزرو غذا', callback_data=0),
            InlineKeyboardButton('کتابخانه', callback_data=1),
        ],
        [
            InlineKeyboardButton('بوک‌بنک', callback_data=2),
            InlineKeyboardButton('انتخاب واحد', callback_data=3),
        ],
        [
            InlineKeyboardButton('کیف پول', callback_data=4)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(
        settings.MESSAGES['menu'],
        reply_markup=markup
    )

    return settings.STATES['menu']


async def food_reserve(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = query.from_user.id

    keyboard = [
        [
            InlineKeyboardButton('رزرو غذا', callback_data=0),
            InlineKeyboardButton('کتابخانه', callback_data=1),
        ],
        [
            InlineKeyboardButton('بوک‌بنک', callback_data=2),
            InlineKeyboardButton('انتخاب واحد', callback_data=3),
        ],
        [
            InlineKeyboardButton('کیف پول', callback_data=4)
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    food_updater_service = FoodUpdaterService()
    food_cycle = '\n'.join([settings.MESSAGES['menu_food_item'].format(day=weekday_to_persian_weekday(weekday),
                                                                       food=food)
                            for weekday, food in food_updater_service.get_a_food_cycle().items()])
    await query.edit_message_text(
        f"{settings.MESSAGES['menu_food_main']}\n"
        f"{food_cycle}",
        # reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    return settings.STATES['menu']


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
                CallbackQueryHandler(food_reserve, pattern=r'^0$')
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    ))

    application.run_polling()
