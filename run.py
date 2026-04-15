import sys
import os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from main import run

if __name__ == "__main__":
    run()