import csv
import glob
from collections import defaultdict, deque
from math import sqrt
from parser import Parser

from pyvis.network import Network


class CleanData:
    def __init__(self, path):
        graph = Parser(path).gen_graph()
        self.network = graph.to_network()
        self.old_nodes = graph.nodes
        self.adj_dir = self.network.get_adj_list()
        self.zoom = 500
        self.size = 2

        # dict: old_node_id -> caption
        self.caption_dict = {}
        self.new_caption_dict = {}
        self.get_caption_dict()

    # 古いnode_idに対応するcaption_dictを取得
    def get_caption_dict(self):
        for n in self.old_nodes:
            self.caption_dict[n.id] = n.caption

    # 特定のnodeから接続しているnodesを抽出する
    def extract_connected_network(self, start_node_id):
        que = deque()
        visited = set()

        # start_node に隣接するnodeを全てqueに入れる
        que.extend(self.adj_dir[start_node_id])

        while len(que) > 0:
            cur_id = que.pop()
            visited.add(cur_id)
            # (TODO) 関数neighborsに変更
            # https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.neighbors
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
            self.new_caption_dict[new_id] = self.caption_dict[old_id]
            old_node = self.network.get_node(old_id)

            # add new node to new network
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

        return new_network

    def to_html(self, network, fname="test.html"):
        network.write_html(fname)

    def to_csv(self, network, fname="test.csv"):
        """
        convert pyvis.Network to csv files
        """
        meta_nodes = defaultdict(list)

        with open(fname, "w") as f:
            writer = csv.writer(f)

            # nodes info
            nodes = network.get_nodes()
            writer.writerow(["#nodes", len(nodes)])

            for node_id in nodes:
                node = network.get_node(node_id)
                meta_nodes[str(node["group"])].append(node_id)

                # node_id, x座標, y座標, meta-node_id, name
                writer.writerow(
                    [
                        node_id,
                        node["x"],
                        node["y"],
                        node["group"],
                        self.new_caption_dict[node_id],
                    ]
                )

            # edges info
            edges = network.get_edges()
            writer.writerow(["#edges", len(edges)])

            for i, edge in enumerate(edges):
                # edge_id, node1_id, node2_id
                writer.writerow([str(i), edge["from"], edge["to"]])

            # clusters info
            writer.writerow(["#clusters", len(meta_nodes.keys())])

            for meta_node_id, (meta_node, children) in enumerate(meta_nodes.items()):
                # id, x, y, r, children
                info = self.calc_meta_node_info(children, network)
                x, y, r = info["x"], info["y"], info["r"]
                meta_node_info = [meta_node_id, x, y, r]
                meta_node_info.extend(children)

                writer.writerow(meta_node_info)

    def calc_meta_node_info(self, children, network, size=2):
        """
        :params: meta_node_id(int): the id of the meta_node
        :params: children(int): list of node(dict) which composes meta_node_id
        :return: dict{"x", "y", "r"}
        """
        info = {}
        minx = 1.0e30
        miny = 1.0e30
        maxx = -1.0e30
        maxy = -1.0e30

        if len(children) == 1:
            # the meta node has only one node
            info["x"] = network.get_node(children[0])["x"]
            info["y"] = network.get_node(children[0])["y"]
            # (TODO) 定数をConstants Classにして、sizeはそこからとる
            # 今は、Craph.pyのto_networkメソッド内のデフォルト引数
            info["r"] = size

        else:
            # メタノードの中で、最小のx、y を算出
            for node_id in children:
                node = network.get_node(node_id)
                x = node["x"]
                y = node["y"]
                minx = minx if minx < x else x
                miny = miny if miny < y else y
                maxx = maxx if maxx > x else x
                maxy = maxy if maxy > y else y

            center_x = (maxx + minx) / 2.0
            center_y = (maxy + miny) / 2.0
            info["x"] = center_x
            info["y"] = center_y
            info["r"] = sqrt((maxx - center_x) ** 2 + (maxy - center_y) ** 2)

        return info


if __name__ == "__main__":
    # csv_files = glob.glob("./result/csv_files/*")

    # for path in csv_files:
    #     clean_data = CleanData(path)

    path = "./result/csv_files/layout0-0.csv"
    clean_data = CleanData(path)
    visited = clean_data.extract_connected_network(1)
    new_network = clean_data.create_cleaned_network(visited)

    clean_data.to_csv(new_network)
