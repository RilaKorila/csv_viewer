from graph import Cluster, Edge, Graph, Node


def get_node_info(data):
    """
    return the set of Node class
    """
    nodes = set()

    for node_info in data:
        node = Node(*node_info)
        nodes.add(node)

    return nodes


def get_edge_info(data):
    """
    return the set of Node class
    """
    edges = set()

    for edge_info in data:
        edge = Edge(*edge_info)
        edges.add(edge)

    return edges


def get_cluster_info(data):
    clusters = set()

    for i in range(0, len(data), 2):
        id, x, y, r = data[i][0:4]
        children = data[i + 1][1:]

        cluster = Cluster(id, x, y, r, children)
        clusters.add(cluster)

    return clusters


def parse_file(data):
    # get node info
    if data[0][0] == "#nodes":
        NODE_NUM = int(data[0][1])
    else:
        raise Exception("Wrong FileTemplate: NODE_NUM not found")
    nodes = get_node_info(data[1 : NODE_NUM + 1])

    # get edge info
    if data[NODE_NUM + 1][0] == "#edges":
        EDGE_NUM = int(data[NODE_NUM + 1][1])
    else:
        print(data[NODE_NUM])
        raise Exception("Wrong FileTemplate: EDGE_NUM not found")
    edges = get_edge_info(data[NODE_NUM + 2 : NODE_NUM + EDGE_NUM + 2])

    # get cluster info
    if data[NODE_NUM + EDGE_NUM + 2][0] == "#clusters":
        CLUSTER_NUM = int(data[NODE_NUM + EDGE_NUM + 2][1])
    else:
        print(data[NODE_NUM + EDGE_NUM + 2])
        raise Exception("Wrong FileTemplate: CLUSTER_NUM not found")

    clusters = get_cluster_info(data[NODE_NUM + EDGE_NUM + 3 :])

    graph = Graph(nodes, edges, clusters)

    return graph
