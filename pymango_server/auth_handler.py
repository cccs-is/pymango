"""Tornado handler for azure access"""
import os
import logging
import requests
import uuid
import msal

from tornado import web
from notebook.base.handlers import APIHandler, IPythonHandler

logger = logging.getLogger(__name__)

AUTHORITY = "https://login.microsoftonline.com/fa9b7bc4-84f2-4ea2-932a-26ca2f5fb014"
CLIENT_ID = "b989b926-a638-488f-b6c9-02d4a0289c14"
CLIENT_SECRET = "[=GPDG?x.hTSWfWxMmJmO08eyb1KFMw6" # Our Quickstart uses this placeholder
SCOPE = ["https://datalake.azure.net/user_impersonation"]

#REDIRECT_PATH = 'http://localhost:8888/azure_auth/callback'
REDIRECT_PATH = 'https://jupyhub.exp.pilot.aadtest.ca/user-redirect/pymango/callback'

class Tokens:

    def __init__(self) -> None:
        self.reset_tokens()

    def reset_tokens(self) -> None:
        self._access_token = None
        self._refresh_token = None

    def set(self, access_token, refresh_token):
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def access_token(self):
        return self._access_token
    
    @property
    def refresh_token(self):
        return self._refresh_token

tokens = Tokens()

class AuthenticateHandler(IPythonHandler):

    @web.authenticated
    def get(self, filepath: str = "") -> None:
        tokens.reset_tokens()
        logger.info('LoginHandler()->get()')
        self.state = str(uuid.uuid4())
        auth_url = _build_auth_url(scopes=[], state=self.state)
        logger.info('in loginHandler() -> auth_url: '+ auth_url)
        # self.write(self.render_template('index.html'))
        # self.write(self.render_template("login.html", auth_url=auth_url, version=msal.__version__))
        self.redirect(auth_url)
        logger.info('+++++++++++')
        pass

    @web.authenticated
    async def put(self, filepath: str = "") -> None:
        logger.info('LoginHandler()->put()')
        pass


class CallbackHandler(IPythonHandler):

    @web.authenticated
    # def get(self, filepath: str = "") -> None:
    #     logger.info('CallbackHandler()->get()')
    #     pass
    def get(self, *args) -> None:
        code = self.get_argument('code')
        logger.info('CallbackHandler()->get()')
        print('args: "', args, '" <<<')
        logger.info('code: "' + code + '" <<<')
        logger.info('+----------+')
        result = _build_msal_app(cache=None).acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=REDIRECT_PATH)
        if "error" in result:
            return render_template("templates/auth_error.html", result=result)
        logger.info('>> in Authorized(1) id_token_claims: ' + str(result.get('id_token_claims')))
        logger.info('>> in authorized(2) access_token   : ' + str(result.get('access_token')))
        logger.info('>> in authorized(3) refresh_token  : ' + str(result.get('refresh_token')))
        tokens.set(str(result.get('access_token')), str(result.get('refresh_token')))
        self.write(self.render_template('index.html'))
        # pass

    @web.authenticated
    async def put(self, *args) -> None:
        logger.info('CallbackHandler()->put()')
        print('args: "', args, '" <<<')
        logger.info('+----------+')
        pass

class GetTokens(IPythonHandler):
    @web.authenticated
    def get(self, *args) -> str:
        logger.info('returning access token: ' + tokens.access_token)
        self.write(tokens.access_token)

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority or AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri = REDIRECT_PATH)
        # prompt='consent')
