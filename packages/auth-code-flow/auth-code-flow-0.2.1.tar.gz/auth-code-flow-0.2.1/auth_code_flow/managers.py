from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlencode

import requests
from requests.sessions import Session

from . import adapters, exceptions


@dataclass
class FlowManager:
    base_uri: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str
    access_token_path: str = "/access_token"
    authorization_path: str = "/authorize"
    grant_type: str = "authorization_code"
    response_type: str = "code"

    def get_authorization_endpoint(self, state: str) -> str:
        return (
            self.base_uri
            + self.authorization_path
            + "?"
            + urlencode(self.get_authorization_endpoint_params(state=state))
        )

    def get_authorization_endpoint_params(self, state: str) -> Dict[str, str]:
        return {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
            "state": state,
        }

    def get_access_token_endpoint(self) -> str:
        return self.base_uri + self.access_token_path

    def get_access_token_endpoint_params(self, code: str, state: str) -> Dict[str, str]:
        return {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "redirect_uri": self.redirect_uri,
            "state": state,
        }

    def fetch_access_token(
        self, code: str, state: str, post_form_data: bool = False, **kwargs
    ):
        with requests.Session() as session:
            session.mount(self.base_uri, adapters.exponential_backoff_adapter)
            return self.perform_fetch(session, code, state, post_form_data, **kwargs)

    def perform_fetch(
        self, session: Session, code: str, state: str, post_form_data: bool, **kwargs
    ):
        kwargs = {"timeout": (5, 5), **kwargs}
        payload = self.get_access_token_endpoint_params(code=code, state=state)
        if post_form_data:
            kwargs["data"] = payload
        else:
            kwargs["json"] = payload

        resp = None
        try:
            resp = session.post(self.get_access_token_endpoint(), **kwargs)
            resp.raise_for_status()
            return resp
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
        ) as exc:
            raise exceptions.AuthCodeFlowError(response=resp) from exc
