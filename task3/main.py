import heapq
import networkx as nx
from graph_data import edges, nodes, nodes_positions
from time import perf_counter
from matplotlib import pyplot as plt
from pathlib import Path


def build_graph(nodes, edges) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)
    return G


def shifted_labels(pos, dx=0.3, dy=0.3) -> dict:
    return {node: (x + dx, y + dy) for node, (x, y) in pos.items()}


def draw_graph(G, positions, filename="ukraine_transport_graph.png") -> None:
    plt.figure(figsize=(14, 10))
    pos = positions
    distances = nx.get_edge_attributes(G, "weight")

    nx.draw(
        G, pos, with_labels=False, node_color="lightblue", node_size=200, font_size=8
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=distances, font_size=6)

    label_pos = shifted_labels(pos, dx=0.2, dy=0.2)
    nx.draw_networkx_labels(G, label_pos, font_size=8)

    plt.title("Graph of Ukrainian Cities and Distances")
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / filename
    plt.savefig(f"{file_path}", dpi=300, bbox_inches="tight")
    plt.show()


def dijkstra(graph, start) -> dict:
    """Реалізація алгоритму Дейкстри з використанням бінарної купи.
    Повертає словник найкоротших відстаней від start_node до всіх інших."""

    # Ініціалізація відстаней
    distances = {node: float("inf") for node in graph.nodes}
    distances[start] = 0

    # Ініціалізація пріоритетної черги
    priority_queue = [(0, start)]  # (відстань, вузол)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Якщо відстань більша за вже знайдену, пропускаємо
        if current_distance > distances[current_node]:
            continue

        # Оновлення відстаней до сусідніх вузлів
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]["weight"]
            distance = current_distance + weight

            # Якщо знайдена коротша відстань, оновлюємо її
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


if __name__ == "__main__":
    graph = build_graph(nodes, edges)
    draw_graph(graph, nodes_positions)
    start_node = "Kyiv"
    print("\nПеревірка з використанням власної реалізації Дейкстри:")
    shortest_paths = dijkstra(graph, start_node)
    print(f"Найкоротші шляхи від {start_node}:")
    for node, distance in shortest_paths.items():
        print(f"До {node}: {distance} км")

    print("\nПеревірка з використанням NetworkX:")
    lengths = nx.single_source_dijkstra_path_length(graph, start_node)
    print(f"Найкоротші шляхи від {start_node}:")
    for node, distance in lengths.items():
        print(f"До {node}: {distance} км")

    # Вимірювання часу виконання власної реалізації
    runs = 100_000
    start_time = perf_counter()
    for _ in range(runs):
        dijkstra(graph, start_node)
    end_time = perf_counter()
    print(
        f"\nСередній час виконання власної реалізації Дейкстри: {(end_time - start_time) / runs:.10f} секунд"
    )
    # Вимірювання часу виконання NetworkX
    start_time = perf_counter()
    for _ in range(runs):
        nx.single_source_dijkstra_path_length(graph, start_node)
    end_time = perf_counter()
    print(
        f"Середній час виконання NetworkX: {(end_time - start_time) / runs:.10f} секунд"
    )
