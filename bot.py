#!/usr/bin/env python

import logging
from telegram import __version__ as TG_VER
from core.models import Student
from django.conf import settings
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

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about university."""
    message = update.message
    user_id = message.from_user.id

    is_registered = False
    if Student.objects.filter(student_id=user_id).exists():
        is_registered = True

    if not is_registered:
        return await register(update, context)

    await menu(update, context)

    return settings.STATES['menu']


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a user with his/her name."""
    message = update.message
    user_id = message.from_user.id

    await message.reply_text(
        settings.MESSAGES['register'],
    )

    return settings.STATES['register_1']


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Register a user with his/her ."""
    message = update.message
    user_id = message.from_user.id

    await message.reply_text(
        settings.MESSAGES['register_1'],
    )

    return settings.STATES['register_2']