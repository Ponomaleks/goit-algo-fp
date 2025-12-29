import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue") -> None:
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node_list_heap, node, pos, x=0, y=0, layer=1) -> nx.DiGraph:
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        index = node_list_heap.index(node)
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(node_list_heap):
            left_node = node_list_heap[left_index]
            graph.add_edge(node.id, left_node.id)
            l = x - 1 / 2**layer
            pos[left_node.id] = (l, y - 1)
            l = add_edges(
                graph, node_list_heap, left_node, pos, x=l, y=y - 1, layer=layer + 1
            )
        if right_index < len(node_list_heap):
            right_node = node_list_heap[right_index]
            graph.add_edge(node.id, right_node.id)
            r = x + 1 / 2**layer
            pos[right_node.id] = (r, y - 1)
            r = add_edges(
                graph, node_list_heap, right_node, pos, x=r, y=y - 1, layer=layer + 1
            )
    return graph


def draw_heap(heap_data: list[int]) -> None:
    tree = nx.DiGraph()
    node_list_heap = list(map(lambda val: Node(val, "skyblue"), heap_data))

    pos = {node_list_heap[0].id: (0, 0)}
    tree = add_edges(tree, node_list_heap, node_list_heap[0], pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors
    )
    plt.show()


if __name__ == "__main__":
    data = [13, 6, 8, 45, 5, 1, 23, 78, 34, 12]

    heapq.heapify(data)
    print("Min-Heap array:", data)

    draw_heap(data)
