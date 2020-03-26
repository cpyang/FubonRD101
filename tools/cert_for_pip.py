# -*- coding: utf-8 -*-
"""
Add MITM CA Certificate to pip.ini 

Assumption: python 2.x or 3.x installed via Anaconda
To do this behind the MITM proxy, only minimal packages are used as pip is not actully useful before this step.

"""
from __future__ import print_function
import sys, os
from socket import socket
from OpenSSL import SSL, crypto

cert_filename = os.path.join(os.getenv('APPDATA'), 'mitm.pen')
pip_config_path = os.path.join(os.getenv('APPDATA'), 'pip')
pip_config_filename = os.path.join(pip_config_path, 'pip.ini')

port = 443
hostname = sys.argv[1] if len(sys.argv) > 1 else 'google.com'

context = SSL.Context(SSL.TLSv1_2_METHOD)
conn = SSL.Connection(context, socket())
certs = []

print('connecting %s' % (hostname))
try:
    conn.connect((hostname, port))
    conn.do_handshake()
    certs = conn.get_peer_cert_chain()
except SSL.Error as e:
    print(str(e))
    exit(1)

cert = certs[1]
cert_components = dict(cert.get_subject().get_components())
cn = (cert_components.get(b'CN')).decode('utf-8')
print('cert: %s' % (cn))

try:
    with open(cert_filename, 'w+') as f:
        print('writing %s' % (cert_filename))
        f.write((crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')))
    if not os.path.exists(pip_config_path):
        os.makedirs(pip_config_path)
    with open(pip_config_filename, 'w+') as f:
        print('writing %s' % (pip_config_filename))
        f.write("[global]\ncert = %s\n" % (cert_filename))
except IOError as e:
    print(str(e))
    exit(1)
