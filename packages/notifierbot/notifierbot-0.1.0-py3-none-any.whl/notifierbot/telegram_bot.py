"""
Telegram Notification Bot
"""

import requests

class TelegramConfig:
    """
    Configuration Variable for Telegram Bot

    Parameters
    ---
    bot_token: BOT TOKEN recieved from @botfather

    chat_id: CHAT ID received from https://api.telegram.org/bot{BOT_TOKEN}/getUpdates
    """
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

class TelegramBot:
    """
    API for Telegram Bot

    Parameters
    ---
    config: TelegramConfig object
    """
    def __init__(self, config: TelegramConfig):
        self.bot_token = config.bot_token
        self.chat_id = config.chat_id

    def add_message(self, message):
        """
        Function to add a message to notification

        Parameters
        ---
        message: Message to be passed in notification
        """
        self.message = message

    def notify(self):
        """
        Function to send a notification

        Parameters
        ---
        None
        """
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text="{self.message}"'
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)