import glob
from collections import deque
from parser import Parser
from tokenize import group

from pyvis.network import Network


class CleanData:
    def __init__(self, path):
        graph = Parser(path).gen_graph()
        self.network = graph.to_network()
        self.adj_dir = self.network.get_adj_list()
        self.zoom = 500
        self.size = 2

    # 特定のnodeから接続しているnodesを抽出する
    def extract_connected_network(self, start_node_id):
        que = deque()
        visited = set()

        # start_node に隣接するnodeを全てqueに入れる
        que.extend(self.adj_dir[start_node_id])

        while len(que) > 0:
            cur_id = que.pop()
            visited.add(cur_id)

            neighbors = self.adj_dir[cur_id]

            for node in neighbors:
                if not node in visited:
                    que.append(node)

        print("BFS探索終了")
        # print(visited)

        return visited

    def create_cleaned_network(self, visited):
        """
        assign new node id after cleaning up the old network
        """
        new_network = Network()
        nodes = []
        node_id_converter = {}

        # add nodes to new network
        for new_id, old_id in enumerate(visited):
            node_id_converter[old_id] = new_id
            old_node = self.network.get_node(old_id)
            new_network.add_node(
                n_id=new_id,
                group=old_node["group"],
                borderWidth=0,
                x=old_node["x"],
                y=old_node["y"],
                color=old_node["color"],
                size=old_node["size"],
            )
            nodes.append(old_node["group"])

        print("-- new network --")
        print("num node: ", len(nodes))
        print("num meta-node: ", len(set(nodes)))

        ## add edges to new network
        edges = self.network.get_edges()
        for edge in edges:
            try:
                if edge["from"] in visited or edge["to"] in visited:
                    node_1 = node_id_converter[edge["from"]]
                    node_2 = node_id_converter[edge["to"]]
                    new_network.add_edge(node_1, node_2, width=0.2)

            except AssertionError:
                print("AssertionError: ", edge["from"], " | ", edge["to"])
                continue

        new_network.inherit_edge_colors(False)
        new_network.toggle_drag_nodes(False)
        new_network.toggle_physics(False)
        new_network.toggle_stabilization(False)

        self.new_network = new_network

    def to_html(self, network, fname="test.html"):
        network.write_html(fname)


if __name__ == "__main__":
    # csv_files = glob.glob("./result/csv_files/*")

    # for path in csv_files:
    #     clean_data = CleanData(path)

    path = "./result/csv_files/layout0-0.csv"
    clean_data = CleanData(path)
    visited = clean_data.extract_connected_network(1)
    clean_data.create_cleaned_network(visited)
