#!/usr/bin/env python3

import os
import ssl
import socket
import logging
import argparse
import tempfile
import traceback
from threading import Thread

def parse_addr(addr):
    if ':' not in addr:
        addr = '127.0.0.1:' + addr
    host, port = addr.rsplit(':', 1)
    port = int(port)
    return host, port

def load_cert(context):
    crtfile = tempfile.mktemp(suffix='.pem')
    keyfile = tempfile.mktemp(suffix='.key')
    os.system(f'openssl req -subj /CN=localhost -new -x509 -days 365 -nodes -out {crtfile} -keyout {keyfile}')
    context.load_cert_chain(crtfile, keyfile)

def handle_client(sconn, backend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bconn:
        bconn.connect(parse_addr(backend))
        print("backend conn established")
        Thread(target=scat, args=(sconn, bconn)).start()
        scat(bconn,sconn)

def scat(sconn, dconn):
    while True:
        try:
            r = sconn.recv(512)
            if r:
                dconn.sendall(r)
        except:
            traceback.print_exc()
            break
    
def sslify(addr, backend):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(parse_addr(addr))
        s.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        load_cert(context)

        with context.wrap_socket(s, server_side=True) as ssock:
            logging.debug(ssock.version())
            while True:
                try:
                    conn, address = ssock.accept()
                    print('client established conn')
                    Thread(target=handle_client, args=(conn, backend)).start()
                except KeyboardInterrupt:
                    break
                except:
                    traceback.print_exc()

                #logging.info('conn established')

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("server")
    ap.add_argument("backend")
    return ap.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    sslify(args.server, args.backend)
