import random
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import Dict
from pathlib import Path


def roll_dice(num_rolls) -> Dict[int, int]:
    sum_counts = defaultdict(int)

    for _ in range(num_rolls):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        sum_counts[total] += 1

    return sum_counts


def calculate_probabilities(sum_counts, num_rolls) -> Dict[int, float]:
    probabilities = {}
    for total in range(2, 13):
        probabilities[total] = sum_counts[total] / num_rolls
    return probabilities


def plot_probabilities(probabilities, filename="dice_probabilities.png") -> None:
    sums = list(probabilities.keys())
    probs = list(probabilities.values())

    plt.bar(sums, probs, color="blue", alpha=0.7)
    plt.xlabel("Сума на кубиках")
    plt.ylabel("Імовірність")
    plt.title("Імовірності сум при киданні двох кубиків")
    plt.xticks(sums)
    plt.ylim(0, max(probs) + 0.05)
    plt.grid(axis="y")
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / filename
    plt.savefig(f"{file_path}", dpi=300, bbox_inches="tight")
    plt.show()


def main() -> None:
    num_rolls = 100000
    sum_counts = roll_dice(num_rolls)
    probabilities = calculate_probabilities(sum_counts, num_rolls)

    print("Сума - Імовірність")
    for total in range(2, 13):
        print(f"{total} - {probabilities[total]:.4f}")

    plot_probabilities(probabilities)


if __name__ == "__main__":
    main()
