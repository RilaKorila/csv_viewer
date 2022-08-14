from pyvis.network import Network


class Node:
    def __init__(self, id, x, y, cluster_id, caption=""):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.cluster_id = int(cluster_id)
        self.caption = caption


class Edge:
    def __init__(self, node1, node2):
        self.node1 = int(node1)
        self.node2 = int(node2)


class Cluster:
    def __init__(self, id, x, y, r, children):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)
        self.children = set()
        for child_id in children:
            self.children.add(int(child_id))


class Graph:
    def __init__(self, nodes, edges, clusters):
        self.nodes = nodes
        self.edges = edges
        self.clusters = clusters

    def draw(self, size=1, zoom=50):
        """
        draw a graph with pyvis, and return a html file
        """
        net = Network()

        for node in self.nodes:
            net.add_node(node.id, x=node.x * zoom, y=node.y * zoom, size=size)

        net.toggle_drag_nodes(False)
        net.toggle_physics(False)
        net.toggle_stabilization(False)

        net.show("test.html")
