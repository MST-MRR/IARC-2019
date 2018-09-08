import sys
import getopt

from ProGraphs import Grapher

def main(argv):
    will_pan = False;
    pan_window = -1;

    try:
        opts, args = getopt.getopt(argv, 
                "p:s:", 
                ["pan=", 
                "save=", 
                "pitch=", 
                "yaw=" , 
                "roll="])
    except getopt.GetoptError:
        print('GraphTest.py -p <pan_window>')
        sys.exit()
    for opt, arg in opts:
        if opt in ("-p", "--pan"):
            will_pan = True;
            # catch error if cast fails?
            pan_window = int(arg)
        elif opt in ("-s", "--save"):
            print(arg)
        elif opt == "--pitch":
            print(arg)
        elif opt == "--yaw":
            print(arg)
        elif opt == "--roll":
            print(arg)

    print("Pan is activated: ", will_pan)
    print("Pan window: ", pan_window)
""" #Uncomment this to test the graph
    if pan_window > 0:
        test_grapher = Grapher(pan_window)
        test_grapher.run()
    else:
        test_grapher = Grapher()
        test_grapher.run()
"""
if __name__ == "__main__":
    main(sys.argv[1:])
