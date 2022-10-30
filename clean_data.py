import glob
from collections import deque
from tokenize import group
from parser import Parser

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

        print("探索終了")
        print(visited)

        return visited

    def create_cleaned_network(self, visited):
        """
        assign new node id after cleaning up the old network
        """
        new_network = Network()
        
        for new_id, old_id in enumerate(visited):
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
            
        self.new_network = new_network
        fname = "test.html"
        new_network.write_html(fname)
            
            # new_network.add_node(new_id,
            #                     xxgroup=node.cluster_id,
            #     # label=str(node.cluster_id),
            #     borderWidth=0,
            #     x=node.x * zoom,
            #     y=node.y * zoom,
            #     color=color_dict[node.cluster_id],
            #     size=size,
            # )
        
        

if __name__ == "__main__":
    # csv_files = glob.glob("./result/csv_files/*")

    # for path in csv_files:
    #     clean_data = CleanData(path)

    path = "./result/csv_files/layout0-0.csv"
    clean_data = CleanData(path)
    visited = clean_data.extract_connected_network(1)
    print("------")
    clean_data.create_cleaned_network(visited)
