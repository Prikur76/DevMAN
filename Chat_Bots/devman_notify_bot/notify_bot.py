import os
import logging

from telegram import (
    Bot,
    Update,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hello, {user.mention_markdown_v2()}\!',
    )


def something_with_inline():
    keyboard = [
        [
            InlineKeyboardButton("Что нового", callback_data='1'),
            InlineKeyboardButton("Что пройдено", callback_data='2'),
        ],
        [InlineKeyboardButton("Что дальше", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Используйте /start для теста бота')


def main() -> None:
    load_dotenv()
    tg_token = os.environ.get('TG_TOKEN')
    bot = Bot(token=tg_token)

    bot.send_message(chat_id=283111606, text="I'm sorry Dave I'm afraid I can't do that.")

    updater = Updater(token=tg_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()