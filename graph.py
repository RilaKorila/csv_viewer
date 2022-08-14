from pyvis.network import Network


class Node:
    def __init__(self, id, x, y, cluster_id, caption=""):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.cluster_id = int(cluster_id)
        self.caption = caption


class Edge:
    def __init__(self, id, node1, node2):
        self.id = int(id)
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

    def to_network(self, size=2, zoom=200):
        """
        draw a graph with pyvis, and return a html file
        """
        network = Network()

        for node in self.nodes:
            network.add_node(
                node.id,
                group=node.cluster_id,
                borderWidth=0,
                x=node.x * zoom,
                y=node.y * zoom,
                size=size,
            )

        for edge in self.edges:
            try:
                network.add_edge(edge.node1, edge.node2, width=0.2)
            except AssertionError:
                print(edge.node1, " と ", edge.node2)
                continue

        network.inherit_edge_colors(False)
        network.toggle_drag_nodes(False)
        network.toggle_physics(False)
        network.toggle_stabilization(False)

        return network

    def to_html(self, fname="test.html"):
        network = self.to_network()
        network.write_html(fname)

        return network.html
