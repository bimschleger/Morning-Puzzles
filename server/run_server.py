#!/usr/bin/env python3
"""
Convenience runner for Morning Puzzles API server.
Usage:
    python3 run_server.py [port]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import run_standalone_server

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_standalone_server(port=port)
