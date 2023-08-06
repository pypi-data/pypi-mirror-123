import zlib
import sys

def main():
    sys.stdout.buffer.write(zlib.compress(sys.stdin.buffer.read()))