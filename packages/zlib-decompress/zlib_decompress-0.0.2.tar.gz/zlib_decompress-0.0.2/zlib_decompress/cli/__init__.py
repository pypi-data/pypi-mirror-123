import zlib
import sys

def main():
    print(zlib.decompress(sys.stdin.buffer.read()).decode(), end='')
