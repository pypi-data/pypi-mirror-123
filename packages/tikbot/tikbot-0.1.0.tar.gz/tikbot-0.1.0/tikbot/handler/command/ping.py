from telegram import Update
from telegram.ext import CallbackContext
from typing import Dict, List, Tuple

from tikbot.apiros import ApiRos

message = f"""
ping <ip> <count>
"""


def res_to_str(responses: List[Tuple[str, Dict[str, str]]]):
    messages: List[str] = [
        "Seq, Host, Size, TTL, Time, Sent, Received, Loss, Min, Avg, Max"
    ]
    for status, response in responses:
        if status == "!done":
            break
        messages.append(", ".join(list(response.values())))
    return "\n".join(messages)


def ping(update: Update, context: CallbackContext):
    if not context.args or len(context.args) != 2:
        update.effective_message.reply_text(message)
        return
    api: ApiRos = context.bot_data["ROS"]
    ip, c = context.args
    if not c.isdigit():
        update.effective_message.reply_text(message)
        return
    res = api.talk(["/ping", f"=address={ip}", f"=count={c}"])
    update.effective_message.reply_text(res_to_str(res))
