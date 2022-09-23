import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

## config
st.set_page_config(layout="wide")

## constans
GRAPH_MAX = 19
GRAPH_MIN = 0
GEN_MAX = 9
GEN_MIN = 0


def each_graph():
    ## sidebar
    with st.sidebar:
        graph_no = st.number_input(
            "グラフ番号", step=1, min_value=GRAPH_MIN, max_value=GRAPH_MAX
        )
        gen_no = st.number_input("世代番号", step=1, min_value=GEN_MIN, max_value=GEN_MAX)

        st.markdown("----")
        st.write("グラフ番号: ", graph_no)
        st.write("世代番号: ", gen_no)

    ## main contents
    st.title("Graph Viewer")

    path = "./result/html_files/layout" + str(gen_no) + "-" + str(graph_no) + ".html"
    with open(path) as f:
        _html = f.read()
        components.html(_html, height=800, width=800)


def compare():
    ## sidebar
    with st.sidebar:
        graph_no = st.number_input(
            "グラフ番号", step=1, min_value=GRAPH_MIN, max_value=GRAPH_MAX
        )

        st.markdown("----")
        st.write("グラフ番号: ", graph_no)

    ## main contents
    st.title("Compare Graph")

    image = Image.open("pareto.png")
    st.image(image, caption="Pareto Front")

    # Initialグラフ と Optimizedグラフを横並びで表示
    left, right = st.columns(2)

    with left:
        st.markdown("### Initial Graph")
        init_path = "./result/html_files/layout0-" + str(graph_no) + ".html"
        with open(init_path) as f:
            _html = f.read()
            components.html(_html, height=800, width=800)

    with right:
        st.markdown("### Optimized Graph")
        optimized_path = "./result/html_files/layout9-" + str(graph_no) + ".html"
        with open(optimized_path) as f:
            _html = f.read()
            components.html(_html, height=800, width=800)


def main():
    st.sidebar.markdown("## ページ切り替え")
    ## menuを選択
    menu = st.sidebar.radio("メニュー", ("each graph", "compare"))

    # --- page振り分け
    if menu == "each graph":
        each_graph()
    else:
        compare()


## メイン
main()
