#!/usr/bin/env python3
from model import URDFModel
import time
def main():
    model = URDFModel("aelos.urdf")
    while True:
        model.step()
        time.sleep(0.005)

if __name__ == "__main__":
    main()