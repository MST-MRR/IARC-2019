#!/bin/bash
clear
g++ -std=c++17 -Wall main.cpp loader.cpp -L/usr/local/lib -lglfw -pthread -lGLEW -lGLU -lGL -lrt -lXrandr -lXxf86vm -lXi -lXinerama -lX11 -o OpenGLExample
./OpenGLExample
