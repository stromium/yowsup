from layers.auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from layers.coder              import YowCoderLayer
from layers.network            import YowNetworkLayer, NetworkError
from stacks import YowBasicStack
import asyncore, sys, traceback, base64



ENDPOINT_REMOTE = ("c2.whatsapp.net", 443)
ENDPOINT_LOCAL = ("127.0.0.1", 9002)
AUTH_CREDENTIALS = ("491632092557", "7pTomcW7GgC9zDt4FKZCMukzs1w=")

def getCredentials():
     password = base64.b64decode(bytes(AUTH_CREDENTIALS[1].encode('utf-8')))
     return (AUTH_CREDENTIALS[0], password)

class YowStackInit:
    def __init__(self):
        #set props
        YowAuthenticatorLayer.setProp("credentials", getCredentials())
        YowNetworkLayer.setProp("endpoint", ENDPOINT_REMOTE)
        YowCoderLayer.setProp("domain", "s.whatsapp.net")
        YowCoderLayer.setProp("resource", "S40-2.12.15")

        stack = YowBasicStack()
        stack.construct()
        stack.sendInitSignal()

        try:
            asyncore.loop()
        except NetworkError, e:
            print("NetworkError, reason: %s, exiting" % e)
            sys.exit(1)
        except AuthError, e:
            print("Auth Error, reason %s" % e)
            sys.exit(1)
        except KeyboardInterrupt, e:
            print("\nYowsdown")
            sys.exit(0)

