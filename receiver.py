from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.error import ConnectionDone
from twisted.protocols.basic import LineOnlyReceiver
import sys
from conf import *
from session_inspector import SessionInspectorMemcache

class InspectorReceiver(LineOnlyReceiver):
  delimiter = '\r\n'
  
  def __init__(self):
    self.inspector = SessionInspectorMemcache()
  
  def connectionMade(self):
    self.peer = self.transport.getPeer()
    self.peerAddr = "%s:%d" % (self.peer.host, self.peer.port)
    print("%s connection with %s established" % (self.__class__.__name__, self.peerAddr))
  
  def connectionLost(self, reason):
    if reason.check(ConnectionDone):
      print("%s connection with %s closed cleanly" % (self.__class__.__name__, self.peerAddr))
    else:
      print("%s connection with %s lost: %s" % (self.__class__.__name__, self.peerAddr, reason.value))
  
  def isAuth(self, is_auth):
    self.transport.write("%d\r\n" % (is_auth, ))

  def lineReceived(self, line):
    try:
      values = line.strip().split()
      
      if len(values) < 1:
        pass
        
      if values[0] == 'isauth' and len(values) > 1:
        for key in values[1:]:
          self.isAuth(self.inspector.isauth(key))
              
      elif values[0] == 'quit':
        self.transport.loseConnection()
      else:
        raise Exception('Invalid command')
    except Exception as inst:
      print type(inst)
      print inst.args
      print inst
      print('invalid line received from client %s' % self.peerAddr)
      return
      
def startListener(interface, port, protocol):
  factory = Factory()
  factory.protocol = protocol
  return reactor.listenTCP( int(port), factory, interface=interface )

startListener(INSPECTOR_INTERFACE, INSPECTOR_PORT, InspectorReceiver)

reactor.run()