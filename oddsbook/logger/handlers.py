import os
import telegram
from logging import Handler, LogRecord


class TelegramBotHandler(Handler):
    def __init__(self):
        super().__init__()
        self.token = os.environ.get('TELEGRAMBOT_TOKEN')
        self.chat_id = os.environ.get('TELEGRAMBOT_CHATID')

    def emit(self, record: LogRecord):
        bot = telegram.Bot(token=self.token)
        bot.send_message(
            self.chat_id,
            self.format(record)
        )