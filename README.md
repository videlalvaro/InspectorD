Usage
-----

    python session_inspector.py

Commands:
---------

isauth
======
  
    isauth session_id1 session_id2 session_id3

returns 0 or 1 if the user of that session id is authenticated
each line of the response corresponds to one of the key passed
the lines are ended by \r\n


quit
====

closes the connection to the server


sample session:
---------------

    telnet localhost 3002
    isauth session_id
    0
    isauth session_ida
    1
    isauth session_ida session_idb session_idc
    1
    0
    1
    quit