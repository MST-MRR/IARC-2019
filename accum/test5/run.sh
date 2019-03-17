#!/bin/bash
clear
g++ -std=c++17 -Wall main.cpp loader.cpp -ggdb -g -lglfw -lGL -lGLEW -lfreeimage -o OpenGLExample
./OpenGLExample
