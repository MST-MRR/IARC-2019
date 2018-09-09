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
    save_dest = 'none'
    graph = []

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
            save_dest = arg + ".png"
        elif opt == "--pitch":
            graph.append(('pitch', int(arg)))
        elif opt == "--yaw":
            graph.append(('yaw', int(arg)))
        elif opt == "--roll":
            graph.append(('roll', int(arg)))

    if not graph:
        print("Nothing to graph!")
        print(usage_string)
        sys.exit()

    if will_pan:
        if save_dest != 'none':
            test_grapher = Grapher(pan=pan_window, save=save_dest, graph=graph)
            test_grapher.run()
        else:
            test_grapher = Grapher(pan=pan_window, graph=graph)
            test_grapher.run() 
    else:
        if save_dest != 'none':
            test_grapher = Grapher(save=save_dest, graph=graph)
            test_grapher.run()
        else:
            test_grapher = Grapher(graph=graph)
            test_grapher.run() 
 

if __name__ == "__main__":
    main(sys.argv[1:])
