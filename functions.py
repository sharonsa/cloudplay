# Scripts for Cloud automation 
# By Sharon Saadon - sharonsaa@gmail.com

def is_ip(str):
    import socket
    try:
        socket.inet_aton(str)
        isip=True
    except socket.error:
        isip=False
    return isip

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

