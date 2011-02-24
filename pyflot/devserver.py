import os


def get_test_page(graph):
    """Renders a test page"""
    templatefile = open(os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            'templates', 
                            'test_page.html'))
    template = templatefile.read()
    template = template.replace("{{ graph.series_json|safe }}", 
                                graph.series_json)
    template = template.replace("{{ graph.options_json|safe }}", 
                                graph.options_json)
    out = open(os.path.join(os.getcwd(), 'testgraph.html'), 'w')
    out.write(template)
    out.close()
