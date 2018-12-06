# Inter-process Communication IARC-2019
A tool to allow python 2.7 processes to send data to the data splitter running in python 3.6.
The data splitter is a tool made to send data to both the real time graphing and logging tools
concurrently.

## Configuration
The interprocess communication should be run from within the tools directory or in the directory 
containing tools. If that is not the case, in IPC.__init__ the filename variable should be changed.

## Operating
Sometimes doesn't run on first try!

The IPC object has multiple parameters

    reader: default=True, Whether or not to manually read os output from the process.
        (sometimes system readds automatically)
    thread_stop: default=threading.Event, Can input an already being used thread stop or it will auto-generate.

The send function should be used to send a dictionary of {data streams: values} to both the logger and RTG.
The alive function will return true if the created process is still running.

May be used in a with statement. 

The quit function must be called if not used within a with statement!

## Troubleshooting
If you have issues or suggestions, message Cole Dieckhaus on slack or email @ csdhv9@mst.edu.