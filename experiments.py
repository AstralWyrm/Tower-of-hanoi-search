"""Reproducible experiment drivers; the search implementations live in hanoi.py."""
import argparse
import json
from pathlib import Path

import hanoi

BASE_DIR = Path(__file__).resolve().parent


def run_case(disks, pegs, algorithm, heuristic="3a", goal="original", moves=False):
    print(f"Searching: d={disks}, p={pegs}, algorithm={algorithm}, heuristic={heuristic}", flush=True)
    solution, expanded = hanoi.solve(disks, pegs, algorithm, heuristic, goal)
    if solution is None:
        raise RuntimeError("No solution found for a solvable experiment")
    result = {
        "disks": disks, "pegs": pegs, "algorithm": algorithm,
        "heuristic": heuristic, "goal": goal,
        "solution_length": len(solution), "expanded_states": expanded,
        "moves": solution,
    }
    print("Solution length:", len(solution))
    if pegs == 3:
        expected = 2 ** disks - 1
        print("Expected length:", expected)
        print("Matches formula:", len(solution) == expected)
        assert len(solution) == expected
    if moves:
        print("Moves:")
        for action in solution:
            print(" (" + action + ")")
    print("Total expanded states:", expanded)
    print()
    return result


def run_ids():
    return run_case(4, 3, "ids", moves=True)


def run_h3a():
    return [run_case(d, 3, "ida", "3a") for d in (4, 5)]


def run_h3b(quick=False):
    return [run_case(d, 3, "ida", "3b", moves=True) for d in ((4, 5) if quick else (4, 5, 6))]


def run_k(quick=False):
    results = [run_case(d, 4, "ids", goal="empty_ends") for d in range(5 if quick else 7)]
    values = [result["solution_length"] for result in results]
    assert values == hanoi.State.k[:len(values)]
    print("k values:", values)
    return results


def run_h4a(quick=False):
    results = [run_case(d, 4, "ida", "4a") for d in range(1, 6 if quick else 8)]
    for result in results:
        assert result["solution_length"] == 2 * hanoi.State.k[result["disks"] - 1] + 1
    print("f(d, 4):", [result["solution_length"] for result in results])
    return results


def main():
    parser = argparse.ArgumentParser(description="Run all Hanoi assignment experiments")
    parser.add_argument("--quick", action="store_true", help="Skip the three largest cases")
    args = parser.parse_args()
    result = {"ids": run_ids(), "h3a": run_h3a(), "h3b": run_h3b(args.quick),
              "k": run_k(args.quick), "h4a": run_h4a(args.quick), "quick": args.quick}
    path = BASE_DIR / "results" / ("quick_results.json" if args.quick else "results.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Saved:", path)


if __name__ == "__main__":
    main()
