#!/usr/bin/env python3

import os
import sys
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

def load_cert(context, certfile, keyfile):
    try:
        context.load_cert_chain(certfile, keyfile)
    except OSError:
        traceback.print_exc()
        print(f'\n\nmaybe try:\nopenssl req -subj /CN=localhost -new -x509 -days 365 -nodes -out {certfile} -keyout {keyfile}\n\n')
        sys.exit(1)

def handle_client(sconn, backend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bconn:
        bconn.connect(backend)
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
    
def tlsify(args):
    bind_addr = parse_addr(args.server)
    back_addr = parse_addr(args.backend)
    certfile = args.cert
    keyfile = args.key

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(bind_addr)
        s.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        load_cert(context, certfile, keyfile)

        with context.wrap_socket(s, server_side=True) as ssock:
            logging.debug(ssock.version())
            while True:
                try:
                    conn, address = ssock.accept()
                    print('client established conn')
                    Thread(target=handle_client, args=(conn, back_addr)).start()
                except KeyboardInterrupt:
                    break
                except:
                    traceback.print_exc()

                #logging.info('conn established')

def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("server")
    ap.add_argument("backend")
    ap.add_argument("--cert", default="cert.pem")
    ap.add_argument("--key", default="cert.key")
    return ap.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    tlsify(args)
