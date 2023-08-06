# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auth_code_flow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'urllib3>=1.26.4,<2.0.0']

setup_kwargs = {
    'name': 'auth-code-flow',
    'version': '0.2.0',
    'description': 'Auth Code Flow (`auth-code-flow`) is a utility for obtaining access tokens on behalf of resource owners using the OAuth 2.0 authentication code flow',
    'long_description': "# Auth Code Flow\n\nAuth Code Flow (`auth-code-flow`) is a utility for obtaining access tokens on behalf of resource owners using [the OAuth 2.0 authorization code flow](https://tools.ietf.org/html/rfc6749).\n\n\n## Quick Start\n\nThis is a quick-start tutorial for using `auth-code-flow` to obtain an access token from an OAuth service provider on behalf of its user.\n\nFleshed-out tutorials for doing this using `auth-code-flow` in Python web frameworks like Django and FastAPI are in the works.\n\n### First Things First\n\nWe'll be walking through the process of obtaining an access token from Stack Exchange on behalf of a user of their service. We'll be implementing our utility in conformity with [the Stack Exchange authentication documentation](https://api.stackexchange.com/docs/authentication).\n\nFirst make sure you've created a Stack Exchange developer application, as you'll need a developer app's client id and client secret for this exercise. Please have a look at the answers to [this question on Stack Exchange](https://meta.stackexchange.com/questions/134532/how-do-you-see-what-applications-youve-authorized-on-stack-exchange-with-oauth) if you can't immediately figure out how to create one.\n\n### Install Auth Code Flow\n\nCreate a virtual environment with any tool of your choice, activate it and install `auth-code-flow` into it.\n\nA Windows user may do theirs this way:\n\n* Create a virtual environment\n  ```\n  python -m venv env\n  ```\n\n* Activate the virtual environment\n  ```\n  .\\env\\Scripts\\activate\n  ```\n\n* Install `auth-code-flow` into the virtual environment\n  ```\n  pip install auth-code-flow\n  ```\n\n### Create a Flow Manager\n\n#### Subclass the Abstract Base Flow Manager Class\n\n```python\nfrom auth_code_flow import AbstractBaseFlowManager\n\nclass StackExchangeFlowManager(AbstractBaseFlowManager):\n    pass\n```\n\n#### Configure the Required Attributes\n\n* `access_token_path`\n* `authorization_path`\n* `base_uri`\n* `client_id`\n* `client_secret`\n* `redirect_uri`\n* `scope`\n\n```python\nfrom auth_code_flow import AbstractBaseFlowManager\n\nclass StackExchangeFlowManager(AbstractBaseFlowManager):\n    access_token_path = '/oauth/access_token/json'\n    authorization_path = '/oauth'\n    base_uri = 'https://stackoverflow.com'\n    client_id = 'your stack exchange client id'\n    client_secret = 'your stack exchange client secret'\n    redirect_uri = 'http://localhost:8000/oauth/callback/stackexchange'\n    scope = 'no_expiry'\n```\n\n#### Override Abstract Methods\n\n* `store_user_state()`\n* `check_user_state()`\n\n```python\nfrom auth_code_flow import AbstractBaseFlowManager\n\nclass StackExchangeFlowManager(AbstractBaseFlowManager):\n    access_token_path = '/oauth/access_token/json'\n    authorization_path = '/oauth'\n    base_uri = 'https://stackoverflow.com'\n    client_id = 'your stack exchange client id'\n    client_secret = 'your stack exchange client secret'\n    redirect_uri = 'http://localhost:8000/oauth/callback/stackexchange'\n    scope = 'no_expiry'\n\n    def store_user_state(self, user, state):\n        STORE[user]['state'] = state\n\n    def check_user_state(self, user, state):\n        try:\n            return STORE[user]['state'] == state\n        except KeyError:\n            return False\n```\n\nIn production code you'll most definitely make use of a database instead of a global dictionary constant 😄.\n\n#### Instantiate a Project-wide Manager from this Subclass\n\n```python\nstack_exchange_flow_manager = StackExchangeFlowManager()\n```\n\n### Working with the Flow Manager\n\nFirst thing to do is to make a random state with the manager, store it against the user whose access token you're hoping to fetch, then ask the manager to build the appropriate authorization endpoint for you to send the user to.\n\n```python\nstate = stack_exchange_flow_manager.make_state()\nstack_exchange_flow_manager.store_user_state(user, state)\nauthorization_endpoint = stack_exchange_flow_manager.get_authorization_endpoint(state)\n```\n\nWhen the user clicks on the link to the authorization endpoint, they will be taken to a dedicated page where they can either approve your authorization request or reject it. In any case, Stack Exchange will redirect to your callback uri with an appropriate response for their action.\n\nIn the view method/handler for the callback uri, extract the state and code query parameters sent by Stack Exchange, and fetch the access token with them.\n\n```python\n# this is how we'd get the query parameters in a Django app\nstate = self.request.GET['state']\ncode = self.request.GET['code']\n\nresp = stack_exchange_flow_manager.fetch_access_token(user, code, state, post_form_data=True)\nresp_json = resp.json()\n\nprint(resp_json)\n```\n\nAt the end of the flow, you'd get back something that looks like: `{'access_token': 'yJNAvcyD120SY6lzBDkrWw))'}`.\n\nThat is the user's access token. You can use it to make requests to the Stack Exchange API on behalf of the user.\n",
    'author': 'Mfon Eti-mfon',
    'author_email': 'mfonetimfon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/a-thousand-juniors/auth-code-flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
