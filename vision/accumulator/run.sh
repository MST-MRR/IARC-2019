#!/bin/bash
clear
g++ -std=c++17 -Wall accumulator/source/main.cpp accumulator/source/shader_loader.cpp -ggdb -g -lglfw -lGL -lGLEW -lopencv_core -lopencv_highgui -lopencv_imgproc -o QRDetector.exe
./QRDetector.exe
