from apq import *


#O utput can be put into GPSVisualiser to get a visual representation of the path.

class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class RouteMap:
    """ Sample solutions for first lab on graphs.

        Implements the graph as a map of (vertex,edge-map) pairs.
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self, filename=None):
        """ Create an initial empty graph. """
        self._structure = dict()
        self._structure2 = dict()
        self._structure3 = dict()
        if filename:
            map = self.graphreader(filename)
            self._structure = map._structure
            self._structure2 = map._structure2
            self._structure3 = map._structure3

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        if self.num_vertices() < 100:
            for v in self._structure:
                vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        if self.num_edges() < 100:
            for e in edges:
                estr += str(e) + ' '
        return hstr + vstr + estr

    # -----------------------------------------------------------------------#

    def graphreader(self, filename):
        """ Read and return the route map in filename. """
        graph = RouteMap()
        file = open(filename, 'r')
        entry = file.readline()  # either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            l = file.readline().split()  # split the line to get the latitude and longditude
            co_ordinates = tuple((l[1], l[2]))
            vertex = graph.add_vertex(nodeid, co_ordinates)
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0
        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = graph.get_vertex_by_label(source)
            target = int(file.readline().split()[1])
            tv = graph.get_vertex_by_label(target)
            file.readline()
            length = float(file.readline().split()[1])
            edge = graph.add_edge(sv, tv, length)
            file.readline()  # read the one-way data
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'edges and added into the graph')
        print(graph)
        return graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def get_coordinates(self, v):
        return self._structure2[v]

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        return self._structure3[element]


    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    # ----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element, c_o):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        # add a dictionary that saves the co-ordinates as the value of the key
        self._structure[v] = dict()
        self._structure3[element] = v
        self._structure2[v] = c_o
        return v

    def get_co_ordinates(self, v):
        return self._structure2[v]

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    def _depthFirstSearch(self, v, marked):
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthFirstSearch(w, marked)

    def depthFirstSearch(self, v):
        marked = dict()
        marked[v] = None
        self._depthFirstSearch(v, marked)
        return marked

    # ---------------------------------------------------------------------#

    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    def dijkstra(self, s):
        open = APQ()
        location = dict()
        closed = dict()  # is the datastructure that will be returned
        pred = dict()
        pred[s] = None
        open.add(0, s)  # start off with the source vertex at the cost of zero and add it to the apq
        location[s] = 0
        while open.length() != 0:
            v = open.remove_min()
            c = v.key()
            p = pred.pop(v.value())
            location.pop(v.value())
            closed[v.value()] = (c, p)
            edges = self.get_edges(v.value())  # get all the edges asociated with the vertex
            for e in edges:
                w = e.opposite(v.value())  # w is the opposite vertex in the edge
                if w not in closed.keys():  # if w is not in the final result
                    newcost = e.element() + v.key()  # calculate the newcost
                    if w not in location.keys():  # if it is new place it in pred and in the apq with the newcost
                        pred[w] = v
                        rt = open.add(newcost, w)
                        location[rt.value()] = rt.index()
                    else:  # else if the newcost is smaller than the previous cost update the apq with the newcost
                        w_elem = open.get_elem(w)
                        if newcost < open.get_key(w):
                            pred[w] = v
                            open.update_key(w_elem, newcost)
        return closed

    def read_result(self, result):
        print("type\tlatitude\tlongitude\telement\tcost")
        for elem, cost in result: # gets the latitude and longitude from the dictionary
            lat = self.get_coordinates(elem)[0]
            lon = self.get_coordinates(elem)[1]
            print("W\t" + str(lat) + "\t" + str(lon) + "\t" + str(elem) + "\t" + str(cost))

    def sp(self, s, e):
        paths = self.dijkstra(s)  # Runs dijkstras algorithm
        lst = []
        ls2 = []
        lst.append((e, paths[e][0]))  # start at the destination value and work backwards
        print("length of path: " + str(paths[e][0]))
        t = paths[e][1].value()
        while True:  # This loop places the element and cost of the vertex in a list
            if t == s:
                lst.append((t, 0.0))
                break
            lst.append((t, paths[t][0]))
            t = paths[t][1].value()
        while len(lst) > 0:  # This loop reverses the list so it starts from source to destination
            po = lst.pop()
            ls2.append(po)
        self.read_result(ls2)
        return ls2

# def graphreader(filename): #Provided by the lecturer
#     """ Read and return the route map in filename. """
#     graph = RouteMap()
#     file = open(filename, 'r')
#     entry = file.readline()  # either 'Node' or 'Edge'
#     num = 0
#     while entry == 'Node\n':
#         num += 1
#         nodeid = int(file.readline().split()[1])
#         l = file.readline().split()  # split the line to get the latitude and longditude
#         co_ordinates = tuple((l[1], l[2]))
#         vertex = graph.add_vertex(nodeid, co_ordinates)
#         entry = file.readline()  # either 'Node' or 'Edge'
#     print('Read', num, 'vertices and added into the graph')
#     num = 0
#     while entry == 'Edge\n':
#         num += 1
#         source = int(file.readline().split()[1])
#         sv = graph.get_vertex_by_label(source)
#         target = int(file.readline().split()[1])
#         tv = graph.get_vertex_by_label(target)
#         file.readline()
#         length = float(file.readline().split()[1])
#         edge = graph.add_edge(sv, tv, length)
#         file.readline()  # read the one-way data
#         entry = file.readline()  # either 'Node' or 'Edge'
#     print('Read', num, 'edges and added into the graph')
#     print(graph)
#     return graph
if __name__ == "__main__":
    g = RouteMap("corkCityData.txt")
    source = g.get_vertex_by_label(1669466540) #from WGB to Neptune stadium
    dest = g.get_vertex_by_label(348809726)
    g.sp(source, dest)

