#!/bin/bash
clear
g++ -std=c++17 -Wall main.cpp loader.cpp -ggdb -g -lglfw -lGL -lGLEW -lfreeimage -lopencv_core -lopencv_highgui -lopencv_imgproc -o QRDetector.exe
./QRDetector.exe
