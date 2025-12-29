def greedy_algorithm(items, max_cost) -> tuple[list[str], int, int]:
    sorted_items = sorted(
        items.items(), key=lambda x: x[1]["calories"] / x[1]["cost"], reverse=True
    )
    total_cost = 0
    total_calories = 0
    selected_items = []

    for item, info in sorted_items:
        if total_cost + info["cost"] <= max_cost:
            selected_items.append(item)
            total_cost += info["cost"]
            total_calories += info["calories"]

    return selected_items, total_cost, total_calories


def dynamic_programming(items, max_cost) -> tuple[list[str], int, int]:
    n = len(items)
    dp = [[0 for _ in range(max_cost + 1)] for _ in range(n + 1)]
    item_list = list(items.items())

    for i in range(1, n + 1):
        item, info = item_list[i - 1]
        cost = info["cost"]
        calories = info["calories"]
        for w in range(max_cost + 1):
            if cost <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + calories)
            else:
                dp[i][w] = dp[i - 1][w]

    w = max_cost
    selected_items = []
    total_cost = 0
    total_calories = dp[n][max_cost]

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item, info = item_list[i - 1]
            selected_items.append(item)
            total_cost += info["cost"]
            w -= info["cost"]

    return selected_items, total_cost, total_calories


if __name__ == "__main__":
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }
    max_cost = 100

    greedy_items, greedy_total_cost, greedy_total_calories = greedy_algorithm(
        items, max_cost
    )
    dp_items, dp_total_cost, dp_total_calories = dynamic_programming(items, max_cost)
    print("Greedy Algorithm:")
    print("Selected items:", greedy_items)
    print("Total cost:", greedy_total_cost)
    print("Total calories:", greedy_total_calories)
    print("\nDynamic Programming:")
    print("Selected items:", dp_items)
    print("Total cost:", dp_total_cost)
    print("Total calories:", dp_total_calories)
