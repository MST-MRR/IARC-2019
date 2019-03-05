#!/bin/bash
clear
g++ -std=c++17 -Wall vbo.cpp use_shaders.cpp -ggdb -g -lglfw -lGL -lGLEW -lfreeimage -o OpenGLExample
./OpenGLExample
