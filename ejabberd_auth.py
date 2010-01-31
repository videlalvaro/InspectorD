#!/usr/bin/python
"""
External auth script for ejabberd to authenticate users using InspectorD

The authentication will be made against a memcache server that holds PHP sessions
If the user is logged in your PHP application then it will be logged in your Ejabberd Server.

With your XMPP class you have to loggin the user like this:
nickname = 'user_nickname'
password = 'php_session_id' # can be obtained calling session_id() inside PHP
xmpp.connect(nickname, password)

if there's a session in memcache by that session_id an is authenticated, then it will be able to loggin to Ejabberd.

At the moment this script don't support the isuser command and the setpass is disabled

Ejabberd conf:
{auth_method, external}.
{extauth_program, "/path/to/inspectord/ejabberd_auth.py"}.

CREDITS:
The listening logic is based on iltl@free.fr script for authentication agasint MySQL DBs.
"""

__author__ = "Alvaro Videla <@old_sound>"
__copyright__ = "Copyright 2010, Alvaro Videla"
__license__ = "MIT"
__version__ = "0.1"

########################################################################
#Setup
########################################################################
import sys, logging, struct
from struct import *

from conf import *
from session_inspector import SessionInspectorMemcache

sys.stderr = open('/var/log/ejabberd/extauth_err.log', 'a')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/var/log/ejabberd/extauth.log',
                    filemode='a')
try:
  inspectord = SessionInspectorMemcache()
except:
  logging.debug("Unable to initialize InspectorD!")
logging.info('extauth script started, waiting for ejabberd requests')
class EjabberdInputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
########################################################################
#Declarations
########################################################################
def ejabberd_in():
    logging.debug("trying to read 2 bytes from ejabberd:")
    try:
      input_length = sys.stdin.read(2)
    except IOError:
      logging.debug("ioerror")
    if len(input_length) is not 2:
      logging.debug("ejabberd sent us wrong things!")
      raise EjabberdInputError('Wrong input from ejabberd!')
    logging.debug('got 2 bytes via stdin: %s'%input_length)
    (size,) = unpack('>h', input_length)
    logging.debug('size of data: %i'%size)
    income=sys.stdin.read(size).split(':')
    logging.debug("incoming data: %s"%income)
    return income
def ejabberd_out(bool):
    logging.debug("Ejabberd gets: %s" % bool)
    token = genanswer(bool)
    logging.debug("sent bytes: %#x %#x %#x %#x" % (ord(token[0]), ord(token[1]), ord(token[2]), ord(token[3])))
    sys.stdout.write(token)
    sys.stdout.flush()
def genanswer(bool):
    answer = 0
    if bool:
      answer = 1
    token = pack('>hh', 2, answer)
    return token
def isuser(in_user, in_host):
  return True
def auth(in_user, in_host, password):
  return inspectord.isauth(password)
def log_result(op, in_user, bool):
  if bool:
    logging.info("%s successful for %s"%(op, in_user))
  else:
    logging.info("%s unsuccessful for %s"%(op, in_user))

########################################################################
#Main Loop
########################################################################
while True:
  logging.debug("start of infinite loop")
  try: 
    ejab_request = ejabberd_in()
  except EjabberdInputError, inst:
    logging.info("Exception occured: %s", inst)
    break
  logging.debug('operation: %s'%(ejab_request[0]))
  op_result = False
  if ejab_request[0] == "auth":
    op_result = auth(ejab_request[1], ejab_request[2], ejab_request[3])
    ejabberd_out(op_result)
    log_result(ejab_request[0], ejab_request[1], op_result)
  elif ejab_request[0] == "isuser":
    op_result = isuser(ejab_request[1], ejab_request[2])
    ejabberd_out(op_result)
    log_result(ejab_request[0], ejab_request[1], op_result)
  elif ejab_request[0] == "setpass":
    op_result=False
    ejabberd_out(op_result)
    log_result(ejab_request[0], ejab_request[1], op_result)
logging.debug("end of infinite loop")
logging.info('extauth script terminating')