import argparse
import socket
import statistics
import time

p = argparse.ArgumentParser(description="Minimal http client")
p.add_argument("--host", help=f"Host for request")
p.add_argument("--port", type=int, help=f"Port to connect")
p.add_argument("--n", type=int, help=f"Number of connections to make", default=10)
args = p.parse_args()

times = []
for i in range(args.n):
    start = time.perf_counter()
    with socket.create_connection((args.host, args.port), timeout=4):
        pass
    elapsed = time.perf_counter() - start
    times.append(elapsed * 1000)

print(f"Round trip time (ms) to {args.host}:{args.port} -- min: {min(times):.2f} max: {max(times):.2f} mean: {statistics.mean(times):.2f} stdev: {statistics.stdev(times):.2f}")
