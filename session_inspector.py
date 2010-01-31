import memcache
from PHPUnserialize import *
from conf import *

class SessionInspector():
  
  def __init__(self):
    global prefix, auth_key
    self.prefix = prefix
    self.auth_key = auth_key

  def getData(self, key):
    raise NotImplementedError("getData is an abstract method")

  def isauth(self, key):
    data = self.getData(key)
    if not data:
      return False
    else:
      try:
        session = PHPUnserialize().session_decode(data)
        return session[self.auth_key]
      except:
        return False

class SessionInspectorMemcache(SessionInspector):
  def __init__(self):
    SessionInspector.__init__(self)
    global sessServers
    self.mc = memcache.Client(sessServers, debug=0)

  def getData(self, key):
    return self.mc.get(self.prefix + key)