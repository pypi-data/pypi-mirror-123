# Auth Code Flow

Auth Code Flow (`auth-code-flow`) is a utility for obtaining access tokens on behalf of resource owners using [the OAuth 2.0 authorization code flow](https://tools.ietf.org/html/rfc6749).


## Quick Start

This is a quick-start tutorial for using `auth-code-flow` to obtain an access token from an OAuth service provider on behalf of its user.

Fleshed-out tutorials for doing this using `auth-code-flow` in Python web frameworks like Django and FastAPI are in the works.

### First Things First

We'll be walking through the process of obtaining an access token from Stack Exchange on behalf of a user of their service. We'll be implementing our utility in conformity with [the Stack Exchange authentication documentation](https://api.stackexchange.com/docs/authentication).

First make sure you've created a Stack Exchange developer application, as you'll need a developer app's client id and client secret for this exercise. Please have a look at the answers to [this question on Stack Exchange](https://meta.stackexchange.com/questions/134532/how-do-you-see-what-applications-youve-authorized-on-stack-exchange-with-oauth) if you can't immediately figure out how to create one.

### Install Auth Code Flow

Create a virtual environment with any tool of your choice, activate it and install `auth-code-flow` into it.

A Windows user may do theirs this way:

* Create a virtual environment
  ```
  python -m venv env
  ```

* Activate the virtual environment
  ```
  .\env\Scripts\activate
  ```

* Install `auth-code-flow` into the virtual environment
  ```
  pip install auth-code-flow
  ```

### Create a Flow Manager

#### Subclass the Abstract Base Flow Manager Class

```python
from auth_code_flow import AbstractBaseFlowManager

class StackExchangeFlowManager(AbstractBaseFlowManager):
    pass
```

#### Configure the Required Attributes

* `access_token_path`
* `authorization_path`
* `base_uri`
* `client_id`
* `client_secret`
* `redirect_uri`
* `scope`

```python
from auth_code_flow import AbstractBaseFlowManager

class StackExchangeFlowManager(AbstractBaseFlowManager):
    access_token_path = '/oauth/access_token/json'
    authorization_path = '/oauth'
    base_uri = 'https://stackoverflow.com'
    client_id = 'your stack exchange client id'
    client_secret = 'your stack exchange client secret'
    redirect_uri = 'http://localhost:8000/oauth/callback/stackexchange'
    scope = 'no_expiry'
```

#### Override Abstract Methods

* `store_user_state()`
* `check_user_state()`

```python
from auth_code_flow import AbstractBaseFlowManager

class StackExchangeFlowManager(AbstractBaseFlowManager):
    access_token_path = '/oauth/access_token/json'
    authorization_path = '/oauth'
    base_uri = 'https://stackoverflow.com'
    client_id = 'your stack exchange client id'
    client_secret = 'your stack exchange client secret'
    redirect_uri = 'http://localhost:8000/oauth/callback/stackexchange'
    scope = 'no_expiry'

    def store_user_state(self, user, state):
        STORE[user]['state'] = state

    def check_user_state(self, user, state):
        try:
            return STORE[user]['state'] == state
        except KeyError:
            return False
```

In production code you'll most definitely make use of a database instead of a global dictionary constant 😄.

#### Instantiate a Project-wide Manager from this Subclass

```python
stack_exchange_flow_manager = StackExchangeFlowManager()
```

### Working with the Flow Manager

First thing to do is to make a random state with the manager, store it against the user whose access token you're hoping to fetch, then ask the manager to build the appropriate authorization endpoint for you to send the user to.

```python
state = stack_exchange_flow_manager.make_state()
stack_exchange_flow_manager.store_user_state(user, state)
authorization_endpoint = stack_exchange_flow_manager.get_authorization_endpoint(state)
```

When the user clicks on the link to the authorization endpoint, they will be taken to a dedicated page where they can either approve your authorization request or reject it. In any case, Stack Exchange will redirect to your callback uri with an appropriate response for their action.

In the view method/handler for the callback uri, extract the state and code query parameters sent by Stack Exchange, and fetch the access token with them.

```python
# this is how we'd get the query parameters in a Django app
state = self.request.GET['state']
code = self.request.GET['code']

resp = stack_exchange_flow_manager.fetch_access_token(user, code, state, post_form_data=True)
resp_json = resp.json()

print(resp_json)
```

At the end of the flow, you'd get back something that looks like: `{'access_token': 'yJNAvcyD120SY6lzBDkrWw))'}`.

That is the user's access token. You can use it to make requests to the Stack Exchange API on behalf of the user.
