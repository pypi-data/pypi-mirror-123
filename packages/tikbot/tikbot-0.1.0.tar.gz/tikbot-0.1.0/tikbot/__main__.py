import os
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import Defaults, Updater

from tikbot.apiros import ApiRos
from tikbot.config import Config
from tikbot.handler.command import register_command

load_dotenv()


def start_bot():
    config = Config()
    defaults = Defaults(
        parse_mode=ParseMode.HTML,
    )
    updater = Updater(
        token=config.token or os.getenv("TOKEN"),
        defaults=defaults,
    )
    register_command(updater.dispatcher)
    api_ros = ApiRos(
        dst=os.getenv("IP"),
        port=os.getenv("PORT"),
        hide=False,
    )
    api_ros.login(
        username=os.getenv("USERNAME"),
        pwd=os.getenv("PASSWORD"),
    )
    updater.dispatcher.bot_data["C"] = config
    updater.dispatcher.bot_data["R"] = 0
    updater.dispatcher.bot_data["ROS"] = api_ros
    updater.start_polling()


def main():
    start_bot()


if __name__ == "__main__":
    main()
