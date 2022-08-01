
# TLSIFY a smallest reverse proxy for TLSing	

## Usage

Assume you have a daemon serving on port 8080, e.g.

```
python3 -m http.server 8080
```

Then you can front it with

```
python3 main.py 8443 8080
```

then
```
firefox https://localhost:8443
```

### Certifcate configuration
Either you have a cert.pem and cert.key file present and you can pass them as CLI arguments

```
python3 main.py --cert=cert.pem --key=cert.key 8443 8080
```

Or you can set your certificate and key in TLS\_CERT and TLS\_KEY variables (you may escape newlines as '\n').

```
TLS_CERT="$(cat cert.pem)" TLS_KEY="$(cat cert.key)" python3 main.py 8443 8080
```

## TODO
 * see how IPv6 works
 * handle better when the key is in the .pem file

## BUGS
 * never seems to close connections to backend
