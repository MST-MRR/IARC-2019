

class File_IO:
    def __init__(self):
        pass

    def read(self, filename):
        # TODO - Pull possible(hardcoded) metrics from file and put into checkboxes
        # TODO - Pull in as label: datastreams, func

        return ["Air Speed", "Altitude", "Pitch", "Roll", "Yaw", "xVelocity", "yVelocity", "zVelocity", "Voltage"]

    def write(self, filename, data):
        # TODO - Format saving into xml

        with open(filename, 'w') as g:
            for output in data:
                for key, value in output.items():
                    g.write("{} = {}\n".format(key, str(value)))

                g.write("\n")
