
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

## TODO
 * see how IPv6 works

## BUGS
 * never seems to close connections to backend
