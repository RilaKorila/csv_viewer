import glob
from collections import deque
from parser import Parser

from pyvis.network import Network


class CleanData:
    def __init__(self, path):
        graph = Parser(path).gen_graph()
        self.network = graph.to_network()
        self.adj_dir = self.network.get_adj_list()

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


if __name__ == "__main__":
    # csv_files = glob.glob("./result/csv_files/*")

    # for path in csv_files:
    #     clean_data = CleanData(path)

    path = "./result/csv_files/layout0-0.csv"
    clean_data = CleanData(path)
    clean_data.extract_connected_network(1)
