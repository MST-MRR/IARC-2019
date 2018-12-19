# Tools IARC-2019
## Data Splitter
Starts and sends data to both the logger and ipc(real time grapher).

## Logger
Logs data as it comes in from the drone in real time.

## Inter-process Communication
Allows python 2.7 processes to send data to the data splitter running in python 3.6. Currently runs the Real time grapher.

## Real Time Grapher
Graphs data as it comes in from drone in real time. Run with the inter-process communication.
