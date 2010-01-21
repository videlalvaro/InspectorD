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
    isauth oglnp9phvn8ac04obdqjk6dko3
    0
    isauth bj6sc485t9s46o57qpngod5lm7
    1
    isauth bj6sc485t9s46o57qpngod5lm7 oglnp9phvn8ac04obdqjk6dko3 n63o4uk297c49131dcdg0h7g72
    1
    0
    1
    quit