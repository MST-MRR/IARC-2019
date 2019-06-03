#!/bin/bash
g++ -c -fPIC main.cpp -o qr.o
g++ -c -fPIC shader_loader.cpp -o shader_loader.o
g++ -shared -Wl,-soname,qr.so -o qr.so qr.o shader_loader.o -std=c++17 -Wall -ggdb -g -lglfw -lGL -lGLEW
rm qr.o
python3 py_to_cpp.py

