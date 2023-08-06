from bottle import route, run, view, static_file

graph_lst = []

class graph:

    def __init__(self,name, xaxis):
        self.xaxis = xaxis
        self.name = name
        self.data = {'base' : {'name' : name, 'xaxis' : xaxis}, 'data' : [] } 
    
    def adddata(self,ctype, label, value, backcol = ['grey']):
        dic = {'type' : ctype,'label' : label, 'data' : value, 'backgroundColor' : backcol}
        self.data['data'].append(dic)

    def getgraph(self):
        return self.data
 
@route('/<filename:path>')
def js(filename):
    return static_file('pychartweb/chart.js', root="")

def show(graphs):
    graph_lst = []
    for i in graphs:
        graph_lst.append(i.getgraph())
    @route('/')
    @view('pychartweb/base')
    def hello():
        return dict(graph = graph_lst)
    graphs = graphs
    run(host='localhost', port=8080, debug=True)

