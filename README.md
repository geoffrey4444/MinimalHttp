# Minimal HTTP client

A small Python client for learning how HTTP works. It sends an HTTP/1.1 GET
request over a TCP socket, optionally uses TLS, and prints the request, response
status, headers, and body.

Requires Python 3 and uses only the standard library.

```sh
python3 http.py          # HTTP: httpbingo.org/get on port 80
python3 http.py --ssl    # HTTPS: httpbingo.org/get on port 443
python3 http.py --host example.com --dest / --port 80
python3 http.py --help
```

This is a learning exercise with basic response parsing. It reads until the
server closes the connection and does not decode chunked or compressed bodies.

Licensed under the [MIT License](LICENSE).
