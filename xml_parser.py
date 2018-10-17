

class XML_Parser:
    def __init__(self):
        pass

    def write(self, filename, data):
        with open(filename, 'w') as g:
            for output in data:
                for key, value in output.items():
                    g.write("{} = {}\n".format(key, str(value)))

                g.write("\n")
