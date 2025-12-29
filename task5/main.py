import uuid
import networkx as nx
import matplotlib.pyplot as plt
from typing import Optional
from collections import deque


class Node:
    def __init__(self, key, color="skyblue") -> None:
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1) -> nx.DiGraph:
    if node is not None:
        graph.add_node(
            node.id, color=node.color, label=node.val
        )  # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2**layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2**layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root) -> None:
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {
        node[0]: node[1]["label"] for node in tree.nodes(data=True)
    }  # Використовуйте значення вузла для міток

    plt.figure(figsize=(8, 5))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
        edgecolors="black",
        linewidths=1,
    )
    plt.show()


def dfs_traversal(root: Node) -> list[Node]:
    stack = [root]
    order = []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_traversal(root: Node) -> list[Node]:
    queue = deque([root])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


def assign_colors(traversal_order) -> None:
    n = len(traversal_order)
    for i, node in enumerate(traversal_order):
        intensity = int(255 * i / (n - 1))
        hex_color = f"#{intensity:02x}{intensity:02x}ff"
        node.color = hex_color


def visualize_traversal(root: Node, method: str) -> None:
    if method == "DFS":
        order = dfs_traversal(root)
    elif method == "BFS":
        order = bfs_traversal(root)
    else:
        raise ValueError("Метод повинен бути 'DFS' або 'BFS'.")

    assign_colors(order)
    draw_tree(root)


if __name__ == "__main__":
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.left.left = Node(33)
    root.left.left.right = Node(12)
    root.left.right = Node(10)
    root.left.right.left = Node(17)
    root.left.right.right = Node(26)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.left.left = Node(6)
    root.right.left.right = Node(7)
    root.right.right = Node(2)
    root.right.right.left = Node(14)
    root.right.right.right = Node(76)

    print("Візуалізація обходу в глибину (DFS):")
    visualize_traversal(root, "DFS")

    print("Візуалізація обходу в ширину (BFS):")
    visualize_traversal(root, "BFS")
