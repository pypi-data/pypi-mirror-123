import logging
from typing import Optional

from leiaapi.generated import ApiClient, ApplicationApi, Application, LoginToken
from .scheduler import scheduled, Scheduler

logger = logging.getLogger(__name__)

TIME_BETWEEN_TOKEN_UPDATE = 300


class SessionManager:
    DEFAULT_SESSION: 'SessionManager' = None

    def __init__(self, api_key: str, client: Optional[ApiClient] = ApiClient(), auto_update_token: bool=True):
        """
        Create a SessionManager to manage the session with Leia.io
        :param api_key: The API Key to connect to api.leia.io
        :param client: A ApiClient object configure with the information of the server
        :param auto_update_token: Set to False to not update the token validity automatically
        """
        super().__init__()
        self._api_key: str = api_key
        self._client: Optional[ApiClient] = client
        self._token: Optional[str] = None
        self._application_api: ApplicationApi = ApplicationApi(api_client=self.client)
        self._application: Optional[Application] = None
        self._scheduler: Optional[Scheduler] = None
        self._auto_update_token = auto_update_token

    @property
    def api_key(self):
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, value):
        self._client = value

    @property
    def token(self):
        return self._token

    @property
    def application_api(self):
        return self._application_api

    @property
    def application(self):
        return self._application

    @property
    def scheduler(self):
        return self._scheduler

    def set_as_default(self):
        SessionManager.DEFAULT_SESSION = self
        return self

    def login(self):
        login: LoginToken = self._application_api.login_application(self.api_key)
        self._application: Optional[Application] = login.application
        self._token: Optional[str] = login.token

        if self._auto_update_token:
            @scheduled(TIME_BETWEEN_TOKEN_UPDATE)
            def renew():
                self._application_api.who_am_i(self.token)

            self._scheduler = renew
        return self

    def logout(self):
        if self.scheduler is not None:
            self.scheduler.cancel()
        self._application_api.logout_application(self.token)
        self._token = None
        return self


SessionManager(None, "").set_as_default()
