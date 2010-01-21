INSPECTOR_INTERFACE='0.0.0.0'
INSPECTOR_PORT=3002

# if you have several servers with different weigths, then try something like:
# sessServers = (['127.0.0.1:11211'] * 3) + (['127.0.0.1:11212'] * 5)
# where 3 and 5 are the weigths defined for those servers in Memcache::addServer in PHP
sessServers = ['127.0.0.1:11211']

#memcache key prefix, use '' if none set.
prefix = ''

# key inside the session array that stores if the user is authenticated or not
# for example this is what symfony uses
auth_key = 'symfony/user/sfUser/authenticated'