from telegram import Update
from telegram.ext import CallbackContext
from tikbot.version import __version__

message = f"""
tikbot v{__version__}
"""


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(message)
