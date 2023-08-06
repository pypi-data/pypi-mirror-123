from typing import List
from telegram.ext import CommandHandler, Dispatcher


# Commands
from .ping import ping
from .start import start

COMMANDS: List[CommandHandler] = [
    CommandHandler("start", start),
    CommandHandler("ping", ping),
]


def register_command(dispatcher: Dispatcher):
    for handler in COMMANDS:
        dispatcher.add_handler(handler)
