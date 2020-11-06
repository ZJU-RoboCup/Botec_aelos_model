#!/usr/bin/env python3
from quadruped_model import Jueying
import time
def main():
    model = Jueying()
    while True:
        model.step()
        time.sleep(0.005)

if __name__ == "__main__":
    main()