import logging
import urllib.parse
import webbrowser
from typing import Text

import requests

from cnside.authenticator import AuthenticatorConfig, MiniServer, CallbackData, OAUTHToken

LOGGER = logging.getLogger(__name__)


class Authenticator:
    def __init__(self, config: AuthenticatorConfig):
        self.config = config

    def _open_browser(self) -> Text:
        params = {
            "response_type": "code",
            "scope": "openId",
            "client_id": "cf890130-015c-41b0-bd3d-ea03fa393b41",
            "state": self.config.state,
            "redirect_uri": self.config.redirect_url,
            "code_challenge": self.config.code_challenge,
            "code_challenge_method": self.config.code_challenge_method
        }

        auth_url = self.config.auth_url + "?" + urllib.parse.urlencode(params)

        webbrowser.open(url=auth_url)

        return auth_url

    def _exchange_code_for_token(self, code: Text) -> OAUTHToken:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_url,
            "code_verifier": self.config.code_verifier
        }

        response = requests.post(
            url=self.config.token_url,
            data=data
        )

        # todo: validate status code

        rv = OAUTHToken(**response.json())
        return rv

    def authenticate(self) -> OAUTHToken:
        print("Starting Browser Interactive Authentication...\n")
        server = MiniServer(config=self.config)

        LOGGER.debug("Starting a MiniServer")
        server.start()

        LOGGER.debug("Opening browser and waiting for callback")
        auth_url = self._open_browser()
        print(f"Please continue the authentication process in your browser (Redirecting automatically).\n"
              "If nothing happens, click here: \n\n"
              f"{auth_url}\n")

        callback_data: CallbackData = server.rq.get()

        LOGGER.debug("Stopping MiniServer")
        server.stop()

        LOGGER.debug("Exchanging code for tokens")
        oauth_token = self._exchange_code_for_token(code=callback_data.code)

        LOGGER.debug("Saving token to disk")
        self.config.storage_handler.token.save(oauth_token.dict())

        print("Authenticated!")

        return oauth_token

    def token(self) -> OAUTHToken:
        try:
            token = OAUTHToken(**self.config.storage_handler.token.load())
            # todo: validate that not expired and renew if needed
        except Exception as e:
            raise ValueError("Failed to load token! User is not authenticated.")

        return token
