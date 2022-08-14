import csv
from parser import Parser

import streamlit as st
import streamlit.components.v1 as components

## constans
GRAPH_MAX = 19
GRAPH_MIN = 0
GEN_MAX = 46
GEN_MIN = 0

## sidebar
with st.sidebar:
    graph_no = st.number_input("グラフ番号", step=1, min_value=GRAPH_MIN, max_value=GRAPH_MAX)
    gen_no = st.number_input("世代番号", step=1, min_value=GEN_MIN, max_value=GEN_MAX)

    st.markdown("----")
    st.write("グラフ番号: ", graph_no)
    st.write("世代番号: ", gen_no)

## main contents
st.title("Graph Viewer")

path = "./result/layout" + str(gen_no) + "-" + str(graph_no) + ".csv"
with open(path) as f:
    reader = csv.reader(f)
    l = [row for row in reader]
    _html = Parser(l).gen_graph().to_html()
    components.html(_html, height=800, width=800)
