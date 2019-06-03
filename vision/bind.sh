#!/bin/bash
g++ -c -fPIC main.cpp -o qr.o
g++ -shared -o qr.so qr.o
rm qr.o
python3 py_to_cpp.py

