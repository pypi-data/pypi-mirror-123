enDI OpenID Provider
=================================

This is still a work in progress.

Open Id connect provider based on enDI (http://endi.coop).

Only *Authorization Code Flow* is supported

Getting Started
---------------

Install
........

Install oidc provider in the same virtual environment as endi.

.. code-block:: console

    $VENV/bin/pip install endi_oidc_provider

Configure your development.ini file
....................................

- Ensure the paths to the session files :

  * session.data_dir : path on disk
  * session.lock_dir : path on disk

- Set the connection uri for database access :

  * sqlalchemy.url : the mysql uri to access endi's database

- Configure oidc specific keys (unique salt and oidc endpoint url ):

  * oidc.salt : a unique salt used for encryption
  * oidc.issuer_url : url of the oidc endpoint (like https://myendi.coop/oidc)

Start the service
.................

- $VENV/bin/pserve development.ini


enDI integration
-----------------------

In your enDI's ini file add the following :

.. code-block:: console

    pyramid.includes =
                        ...
                        endi_oidc_provider
                        ...


That's for model registration so that the db startup initialize the tables.

And add the following :

.. code-block:: console

    endi.includes =
                        ...
                        endi_oidc_provider.plugin
                        ...

It adds an administration panel to manage the oidc consumers that access the
API.


Authorization handling
-----------------------

Client's key
.............

You can generate a Client private key through command-line or through the
administration panel https://myendi.coop/admin/oidc/

.. code-block:: console

    oidc-manage <config_uri> clientadd --client=<client> --uri=<redirect_uri> --scopes=<scopes> --cert_salt=<cert_salt> --logout_uri=<logout_uri> --admin_email=<admin_email>


* config_uri : Your ini file
* client: A label for your client
* redirect_uri : The redirect uri has described in the openid connect specifications (The one passed in the Authorize step)
* scopes : The scope the application is requesting (at least the openid scope should be provided) e.g: "openid profile"
* cert_salt : A salt random key that will be used to encrypt the client secret in the database
* logout_uri : The uri to call on global logout (will be called through iframes)
* admin_email: The e-mail of the consumers administrator

After generating both client_id and client_secret. The client app is able to request authentication.
The client secret and client id should be pased to the consumer's admin, they
are mandatory to allow the oidc authentication/authorization.


Authorize Endpoint
~~~~~~~~~~~~~~~~~~~

The client app can call the Authorization url :

https://myoidc_provider.com/oidc/authorize

It authenticates the user and returns an Authorization code in the response.

Token url
~~~~~~~~~~~~~~

Called in the background, the Token endpoint is accessible at the following url :

https://myoidc_provider.com/oidc/token

The RFC : https://tools.ietf.org/html/rfc6749#section-2.3.1

Describes Client Password transmission methods.

Supported client auth method :

* Through request headers : Basic auth tokens are supported
* Through request POST params : client_id and client_secret keys are then expected

In the response you get :

* An access token with mandatory informations
* An id_token JWS encrypted as described in the spec
* Since we use code flow, the id_token also returns the at_hash access_token
  identification key
