import xml.etree.ElementTree as ET
from xml.dom import minidom


def xml_to_string(xml_tag):
    rough_string = ET.tostring(xml_tag, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def parse_config(filename):
    """
    Reads xml config file and returns parsed data.
    Parameters
    ----------
    filename: str
        Filename of desired config file.
    Returns
    -------
    list of parsed graphs
        Parsed data in format [{graph}, {graph}]. The graph dictionary includes output, legend, title, xlabel, ylabel
        and metrics. Metrics is a list of dictionaries including label, color, func, x_stream, y_stream and z_stream.
    """

    #
    # Decode graph
    output = []

    root = ET.parse(filename).getroot()

    for graph in root.findall('graph'):
        output.append({
            'output': graph.get('output'),
            'legend': graph.get('legend'),

            'title': graph.get('title'),
            'xlabel': graph.get('xlabel'),
            'ylabel': graph.get('ylabel'),

            'metrics': []
        })

        for metric in graph.findall('metric'):
            output[-1]['metrics'].append({
                'label': metric.get('label'),

                'color': metric.get('color'),

                'func': metric.get("func"),

                'x_stream': metric.get('x_stream'),
                'y_stream': metric.get('y_stream'),
                'z_stream': metric.get('z_stream')
            })

    return output


def possible_metrics(filename):
    # TODO - Pull possible(hardcoded) metrics from file and put into checkboxes
    # TODO - Pull in as label: datastreams, func

    # Parse -> parse_config(filename)

    return ["Air Speed", "Altitude", "Pitch", "Roll", "Yaw", "xVelocity", "yVelocity", "zVelocity", "Voltage"]


def write_config(filename, data):

    #
    # Encode graph
    desiredgraphs = ET.Element('desiredgraphs')

    for graph in data:
        curr_graph = ET.SubElement(desiredgraphs, 'graph', {key: value for key, value in graph.items() if type(value) is not list and value})
        for key, lst in [(key, value) for key, value in graph.items() if type(value) is list and value]:
            for item in lst:
                curr_item = ET.SubElement(curr_graph, key, {key: value for key, value in item.items() if value})

    with open(filename, 'w') as g:
        g.write(xml_to_string(desiredgraphs))


if __name__ == '__main__':
    write_config('test_config2.xml', parse_config('test_config1.xml'))