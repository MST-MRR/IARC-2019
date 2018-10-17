from xml.etree.ElementTree import parse as parse_xml


def parse_config(filename):
    """
    Reads xml config file and returns parsed data.

    Parameters
    ----------
    filename: str
        Filename of desired config file.

    Returns
    -------
    list of dicts
        Parsed data in format # TODO -----------------------------------------
    """

    output = []

    root = parse_xml(filename).getroot()

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

    print(output)
    return output
