import argparse
from datetime import datetime
import socket

def log(message, appendix=None):
  print(f"{datetime.now()} -- {message}")
  if appendix is not None:
      print(f"****\n{appendix}\n****")

default_dest = "/get"
default_host = "httpbingo.org"
default_port = 80

p = argparse.ArgumentParser(description="Minimal http client")
p.add_argument("--dest", help=f"Destination for get request (default: {default_dest})", default=default_dest)
p.add_argument("--host", help=f"Host for request (default: {default_host})", default=default_host)
p.add_argument("--port", type=int, help=f"Port to connect (default: {default_port})", default=default_port)
args = p.parse_args()

host = args.host
port = args.port
dest = args.dest

info = socket.getaddrinfo(host, port)
log("Address info:", info)

r = "\r\n".join([
    f"GET {dest} HTTP/1.1",
    f"Host: {host}",
    "User-Agent: geoffrey4444-http/0.1",
    "Accept: */*",
    "Connection: close",
    "",
    ""
    ])
log("Sending request:", r)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.settimeout(4)

  log(f"Connecting to {host} on port {port}")
  s.connect((host, port))
  log(f"Connected to {s.getpeername()[0]} on port {s.getpeername()[1]}")
  
  s.sendall(r.encode())
  reply = b''
  bytes_received = None
  
  while bytes_received != b'':
    bytes_received = s.recv(4096)
    reply += bytes_received
  
  response = reply.split(b'\r\n\r\n', 1)
  header_text = response[0].decode().splitlines()
  status = header_text[0].split()
  headers = {}
  for header in header_text[1:]:
      name, value = header.split(": ", 1)
      headers[name.lower()] = value.strip()
  body = response[-1]
  
  log(f"Host confirms {status[0]}")
  log(f"Status code {status[1]} = {" ".join(status[2:])}")
  log("Headers received:", "\n".join([f"{key}: {headers[key]}" for key in headers]))
  try:
    log("Body received:", body.decode())
  except UnicodeDecodeError:
    log("Body received:", body)




