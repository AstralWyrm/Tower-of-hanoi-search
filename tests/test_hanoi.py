import collections
import unittest

import hanoi


def exact_distances(disks, pegs):
    """Independent breadth-first distances; each tuple entry is a disk's peg."""
    goal = (pegs - 1,) * disks
    distance = {goal: 0}
    queue = collections.deque([goal])
    while queue:
        state = queue.popleft()
        tops = {}
        for disk, peg in enumerate(state):
            tops.setdefault(peg, disk)
        for source, disk in tops.items():
            for target in range(pegs):
                if target == source or (target in tops and tops[target] < disk):
                    continue
                child = list(state)
                child[disk] = target
                child = tuple(child)
                if child not in distance:
                    distance[child] = distance[state] + 1
                    queue.append(child)
    return distance


class HanoiTests(unittest.TestCase):
    def test_ids_counts_and_legal_path(self):
        solution, expanded = hanoi.solve(4, 3, "ids")
        self.assertEqual((len(solution), expanded), (15, 8533))
        pegs = [list(range(1, 5)), [], []]
        for action in solution:
            disk, route = action.split(":")
            source, target = [int(value) - 1 for value in route.split("->")]
            disk = int(disk)
            self.assertEqual(pegs[source][0], disk)
            self.assertTrue(not pegs[target] or disk < pegs[target][0])
            pegs[source].pop(0)
            pegs[target].insert(0, disk)
        self.assertEqual(pegs, [[], [], [1, 2, 3, 4]])

    def test_ida_counts(self):
        for heuristic, count in (("3a", 218), ("3b", 113)):
            solution, expanded = hanoi.solve(4, 3, "ida", heuristic)
            self.assertEqual((len(solution), expanded), (15, count))
        solution, expanded = hanoi.solve(4, 4, "ida", "4a")
        self.assertEqual((len(solution), expanded), (9, 107))

    def test_zero_disks_and_temporary_goal(self):
        for algorithm in ("ids", "ida"):
            self.assertEqual(hanoi.solve(0, 3, algorithm), ([], 0))
        self.assertEqual(len(hanoi.solve(3, 4, "ids", goal="empty_ends")[0]), 4)
        self.assertEqual(hanoi.State.goal_name, "original")

    def test_all_small_states_have_admissible_heuristics(self):
        for pegs, heuristic in ((3, "3a"), (3, "3b"), (4, "4a")):
            disks = 4
            hanoi.State.disks, hanoi.State.pegs = disks, pegs
            hanoi.State.heuristic_name = heuristic
            hanoi.State.goal_name = "original"
            for assignment, distance in exact_distances(disks, pegs).items():
                towers = [[disk + 1 for disk, peg in enumerate(assignment) if peg == p]
                          for p in range(pegs)]
                state = hanoi.State(towers)
                self.assertGreaterEqual(state.h, 0)
                self.assertLessEqual(state.h, distance)
                if heuristic == "3b":
                    self.assertGreaterEqual(state.h, state.heuristic3a())


if __name__ == "__main__":
    unittest.main()
