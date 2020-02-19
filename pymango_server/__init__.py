
"""A Jupyter notebook server extension logging to Azure/Microsoft""" 

import os
from notebook.utils import url_path_join
from .auth_handler import AuthenticateHandler, CallbackHandler, GetTokens


def _jupyter_server_extension_paths():
    return [{"module": "pymango"}]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): 
            handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app

    web_app.settings['jinja2_env'].loader.searchpath += [
        os.path.join(os.path.dirname(__file__), 'templates'),
        os.path.join(os.path.dirname(__file__), 'templates', 'assets'),
    ]

    host_pattern = '.*$'
    base_url = web_app.settings["base_url"]
    print('base_url:', base_url)
    authenticate_path = url_path_join(base_url, 'pymango/authenticate(.*)')
    # callback_path = url_path_join(base_url, 'azure_auth/callback?code=(?P<code>.*)')
    callback_path = url_path_join(base_url, 'pymango/callback(.*)')
    get_tokens_path = url_path_join(base_url, 'pymango/get_tokens(.*)')
    handlers = [
        (authenticate_path, AuthenticateHandler),
	      (callback_path, CallbackHandler),
	      (get_tokens_path, GetTokens)
    ]
    web_app.add_handlers(".*$", handlers)

