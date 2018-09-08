import sys
import getopt

from ProGraphs import Grapher

usage_string = \
'''Usage: <program_name> [-p <pan_window>] [-s <output_file] [--pitch <target>] [--yaw <target>] [--roll <target>]

    -p:       Sets the width of the panning window (in seconds). 
    -s:       Saves graphing output to the specified file.
    --pitch   Creates a subplot for pitch data with target
    --yaw     Creates a subplot for yaw data with target
    --roll    Creates a subplot for roll data with target'''

def main(argv):
    will_pan = False;
    pan_window = -1;

    try:
        opts, args = getopt.getopt(argv, 
                "p:s:", ["pan=", "save=", 
                    "pitch=", "yaw=" , "roll="])
    except getopt.GetoptError:
        print(usage_string)
        sys.exit()
    for opt, arg in opts:
        if opt in ("-p", "--pan"):
            will_pan = True;
            # catch error if cast fails?
            pan_window = int(arg)
        elif opt in ("-s", "--save"):
            # TODO: Implement save feature
            pass
        elif opt == "--pitch":
            # TODO: Implement subplot (same for next two options)
            pass
        elif opt == "--yaw":
            # TODO
            pass
        elif opt == "--roll":
            # TODO
            pass

    print("Pan is activated: ", will_pan)
    print("Pan window: ", pan_window)
    if pan_window > 0:
        test_grapher = Grapher(pan_window)
        test_grapher.run()
    else:
        test_grapher = Grapher()
        test_grapher.run()

if __name__ == "__main__":
    main(sys.argv[1:])
