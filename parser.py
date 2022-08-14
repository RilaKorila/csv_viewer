from graph import Cluster, Edge, Graph, Node


class Parser:
    def __init__(self, data):
        self.data = data
        self.nodes = set()
        self.edges = set()
        self.clusters = set()

    def get_node_info(self, start, end):
        """
        :returns: the set of Node
        """
        for node_info in self.data[start: end]:
            node = Node(*node_info)
            self.nodes.add(node)

    def get_edge_info(self, start, end):
        """
        :returns: the set of Edge
        """
        for edge_info in self.data[start: end]:
            edge = Edge(*edge_info)
            self.edges.add(edge)

    def get_cluster_info(self, start):
        """
        :returns: the set of Cluster
        """
        cluster_data = self.data[start: ]
        for i in range(0, len(cluster_data), 2):
            id, x, y, r = cluster_data[i][0:4]
            children = cluster_data[i + 1][1:]

            cluster = Cluster(id, x, y, r, children)
            self.clusters.add(cluster)

    def gen_graph(self):
        """
        :returns Graph:
        """

        ## get node info
        if self.data[0][0] == "#nodes":
            NODE_NUM = int(self.data[0][1])
        else:
            raise Exception("Wrong FileTemplate: NODE_NUM not found")

        self.get_node_info(1, NODE_NUM + 1)

        ## get edge info
        if self.data[NODE_NUM + 1][0] == "#edges":
            EDGE_NUM = int(self.data[NODE_NUM + 1][1])
        else:
            raise Exception("Wrong FileTemplate: EDGE_NUM not found")

        self.get_edge_info(NODE_NUM + 2, NODE_NUM + EDGE_NUM + 2)

        ## get cluster info
        if self.data[NODE_NUM + EDGE_NUM + 2][0] == "#clusters":
            CLUSTER_NUM = int(self.data[NODE_NUM + EDGE_NUM + 2][1])
        else:
            raise Exception("Wrong FileTemplate: CLUSTER_NUM not found")

        self.get_cluster_info(NODE_NUM + EDGE_NUM + 3)

        return Graph(self.nodes, self.edges, self.clusters)
