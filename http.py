import argparse
from datetime import datetime
import socket
import ssl

def log(message, appendix=None):
  print(f"{datetime.now()} -- {message}")
  if appendix is not None:
      print(f"****\n{appendix}\n****")

def send_and_handle_request(sock, r):
  sock.settimeout(4)

  log(f"Connecting to {host} on port {port}")
  
  sock.connect((host, port))
  
  log(f"Connected to {sock.getpeername()[0]} on port {sock.getpeername()[1]}")

  if (args.ssl):
    log(f"TLS version: {ssock.version()}")
    cipher, tls_version, secret_bits = ssock.cipher()
    log(f"Cipher: {cipher} with TLS version {tls_version} and {secret_bits} secret bits")
  
  sock.sendall(r.encode())
  reply = b''
  bytes_received = None
  
  while bytes_received != b'':
    bytes_received = sock.recv(4096)
    reply += bytes_received
  
  response = reply.split(b'\r\n\r\n', 1)
  header_text = response[0].decode('latin-1').split('\r\n')
  status = header_text[0].split()
  headers = []
  for header in header_text[1:]:
      name, value = header.split(":", 1)
      headers.append((name.lower(), value.strip(' \t')))
  body = response[-1]
  
  log(f"Host confirms {status[0]}")
  log(f"Status code {status[1]} = {' '.join(status[2:])}")
  log("Headers received:", "\n".join([f"{key}: {value}" for key, value in headers]))
  try:
    log("Body received:", body.decode())
  except UnicodeDecodeError:
    log("Body received:", body)


default_dest = "/get"
default_host = "httpbingo.org"

p = argparse.ArgumentParser(description="Minimal http client")
p.add_argument("--dest", help=f"Destination for get request (default: {default_dest})", default=default_dest)
p.add_argument("--host", help=f"Host for request (default: {default_host})", default=default_host)
p.add_argument("--port", type=int, help=f"Port to connect (default: 443 if ssl, otherwise 80)", default=None)
p.add_argument("--ssl", help=f"Connect with SSL if specfied", action="store_true")
args = p.parse_args()

host = args.host
port = args.port if args.port is not None else (443 if args.ssl else 80)
dest = args.dest

info = socket.getaddrinfo(host, port)
log("Address info:", info)

r = "\r\n".join([
    f"GET {dest} HTTP/1.1",
    f"Host: {host}" if args.port is None else f"Host: {host}:{port}",
    "User-Agent: geoffrey4444-http/0.1",
    "Accept: */*",
    "Connection: close",
    "",
    ""
    ])
log("Sending request:", r)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  if args.ssl:
    context = ssl.create_default_context()
    with context.wrap_socket(sock, server_hostname=host) as ssock:
      send_and_handle_request(ssock, r)
  else:
      send_and_handle_request(sock, r)
