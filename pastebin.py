"""
Pastebin manipulation module.

Based on [this code](https://pastebin.com/asRbutde).
"""

from typing import Union

import requests


class PastebinNetworkError(Exception):
    """
    Exception raised when a network request fails.
    """

    message_format = "{r.status_code}"

    def __init__(self, r):
        super().__init__(self.message_format.format(r=r))
        self.r = r


class PastebinLogInError(PastebinNetworkError):
    """
    Exception raised when log in fails.
    """

    message_format = "error logging in: {r.status_code}"


class PastebinPasteError(PastebinNetworkError):
    """
    Exception raised when sending a paste fails.
    """

    message_format = "error sending a paste: {r.status_code}"


class Pastebin:
    """
    Pastebin manipulation class.
    """

    privacy_arguments = {
        "public": 0, "unlisted": 1, "private": 2,  # Originals
        "pub": 0, "u": 1, "unl": 1, "priv": 2,     # Abbreviated
    }

    def __init__(self, dev_key, username, password, debug=False):
        self.dev_key = dev_key
        self.username = username
        self.password = password
        self.debug = debug
        self._api_user_key = None

    @property
    def api_user_key(self) -> str:
        """
        Return API user key, newly created or cached from a previous call.

        :return: API user key, required by other API calls.
        """
        if self._api_user_key is None:
            data = {
                "api_dev_key": self.dev_key,
                "api_user_name": self.username,
                "api_user_password": self.password,
            }
            r = requests.post(
                "https://pastebin.com/api/api_login.php", data=data,
            )
            if 200 <= r.status_code <= 299:
                self._api_user_key = r.text
                if self.debug:
                    print(f"Login status: OK/{r.status_code}")
                    print(f"User token: {self._api_user_key}")
            else:
                if self.debug:
                    print(f"Login status: {r.status_code}")
                raise PastebinLogInError(r)
        return self._api_user_key

    def paste(
        self,
        title: str,
        text: str,
        *,
        text_format: str = "text",
        expire_date: str = "N",
        privacy: Union[int, str] = "private",
    ) -> str:
        """
        Send a paste to Pastebin.

        :param title: The title of the paste.
        :param text: The text to be pasted.
        :param text_format: The format of the pasted text. A list of valid
            values can be found [here](https://pastebin.com/doc_api#5).
        :param expire_date: The time when the paste should expire, as
            explained [here](https://pastebin.com/doc_api#6).
        :param privacy: If `int` (the meanings of these values are described
            [here](https://pastebin.com/doc_api#7)), this is used as given.
            There are no restrictions imposed, allowing the use of any privacy
            values that Pastebin might add in the future. If `str`, it is
            mapped via `self.privacy_arguments` dictionary.
        :return: The URL of the new paste.
        """
        try:
            if not isinstance(privacy, int):
                privacy = self.privacy_arguments[privacy.lower()]
        except (AttributeError, KeyError):
            allowed = ", ".join(
                repr(key) for key in sorted(self.privacy_arguments)
            )
            raise ValueError(
                f"invalid privacy value {repr(privacy)} [allowed: {allowed}]",
            )
        data = {
            "api_option": "paste",
            "api_dev_key": self.dev_key,
            "api_paste_name": title,
            "api_paste_code": text,
            "api_paste_expire_date": expire_date,
            "api_user_key": self.api_user_key,
            "api_paste_format": text_format,
            "api_paste_private": privacy,
        }

        r = requests.post("https://pastebin.com/api/api_post.php", data=data)

        if 200 <= r.status_code < 299:
            if self.debug:
                print("Paste send: OK/200")
                print("Paste URL: ", r.text)
            return r.text
        else:
            if self.debug:
                print(f"Paste send: {r.status_code}")
            raise PastebinPasteError(r)
