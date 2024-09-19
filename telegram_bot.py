"""
This module provides a class to interact with the Telegram Bot API

I will be adding more methods to this class whenever I need them
"""

import requests

class TelegramException(Exception):
    """
    Base exception for the TelegramBot class
    """
    pass

class TelegramBot():
    """
    A class to interact with the Telegram Bot API
    """

    base_url = "https://api.telegram.org/bot"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def __get_url(self, method: str) -> any:
        """
        Helper method to get the URL from the Telegram API

        :param method: The method to call from the Telegram API
        :type method: str
        :return: The response from the API
        :rtype: any
        """
        response = requests.get(
            f"{self.base_url}{self.api_key}/{method}"
        )
        self.__validate_response(response)
        return response.json()["result"]
    
    def __post_url(self, method: str, params: dict[str, any]) -> any:
        """
        Helper method to post the URL from the Telegram API

        :param method: The method to call from the Telegram API
        :type method: str
        :param params: The parameters to send to the API
        :type params: dict[str, any]
        :return: The response from the API
        :rtype: any
        """
        response = requests.post(
            f"{self.base_url}{self.api_key}/{method}",
            params=params
        )
        self.__validate_response(response)
        return response.json()["result"]

    @staticmethod
    def __validate_response(response: requests.Response) -> None:
        """
        Validate the response from the Telegram API

        :param response: The response from the Telegram API
        :type response: requests.Response
        :raises TelegramException: If the response is not OK
        """
        _json_response = response.json()
        if not _json_response["ok"]:
            raise TelegramException(response.text)

    @property
    def api_key(self):
        return self._api_key
    
    def whoami(self) -> dict[str, any]:
        """
        Get information about the bot

        :return: Information about the bot
        :rtype: dict[str, any]
        """
        return self.get_me()
    
    def get_me(self) -> dict[str, any]:
        """
        Get information about the bot

        :return: Information about the bot
        :rtype: dict[str, any]
        """
        return self.__get_url("getMe")

    def get_updates(self) -> list[dict[str, any]]:
        """
        Get updates from the Telegram Bot

        :return: The updates from the Telegram Bot
        :rtype: list[dict[str, any]]
        """
        return self.__get_url("getUpdates")

    def send_message(
        self,
        chat_id: int,
        text: str,
        disable_notification: bool = False
    ) -> bool:
        """
        Send a message to a chat

        :param chat_id: The ID of the chat
        :type chat_id: int
        :param text: The text to send
        :type text: str
        :return: A boolean indicating if the message was sent
        :rtype: bool
        """
        self.__post_url(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "disable_notification": disable_notification
            }
        )
        return True

