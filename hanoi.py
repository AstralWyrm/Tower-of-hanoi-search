#   hanoi.py
#   This code presents the Tower of Hanoi puzzle


class State:

    heuristic_name = "3b"
    goal_name = "original"
    k = [0, 1, 2, 4, 6, 8, 12]

    def __init__(self,a):
        self.a = a
        # Select the heuristic for the current experiment.
        if State.heuristic_name == "3a":
            self.h = self.heuristic3a()
        elif State.heuristic_name == "3b":
            self.h = self.heuristic3b()
        elif State.heuristic_name == "4a":
            self.h = self.heuristic4a()
        else:
            raise ValueError("Unknown heuristic")
        

    def start_state(args):
        State.disks = args.disks
        State.pegs = args.pegs
        a = [list(range(1,args.disks+1))]
        for p in range(args.pegs-1):
            a.append([])
        return(State(a))

    def is_equal_to(self,other):
        return( self.a == other.a )

    def expand( self ):
        children = []
        for p in range(len(self.a)):
            if self.a[p] != []:
                for q in range(len(self.a)):
                    if self.a[q] == [] or self.a[q][0] > self.a[p][0]:
                        child = [peg.copy() for peg in self.a]
                        child[q].insert(0,child[p][0])
                        child[p].pop(0)
                        children.append((State(child), \
                            str(child[q][0])+':'+str(p+1)+'->'+str(q+1),1))
        return children

    def is_goal_old( self ):
        for p in range(len(self.a)-1):
            if self.a[p] != []:
                return False
        return True


    def is_goal(self):
        # Use the temporary goal only for Section 1.3(a).
        if State.goal_name == "empty_ends":
            first_peg = self.a[0]
            final_peg = self.a[-1]
            return first_peg == [] and final_peg == []

        if State.goal_name == "original":
            return self.is_goal_old()

        raise ValueError("Unknown goal")


    def print_action(self,action):
        print(' ('+action+')')

    def print_state( self ):
        print(self.a)

    def heuristic3a( self ):
        for c in range(1,State.disks+1):
            if len(self.a[State.pegs-1]) < c or \
               self.a[State.pegs-1][-c] != 1+State.disks-c:
                return pow(2,State.disks-c)
        return 0

    def heuristic3b(self):
        final_peg = self.a[State.pegs - 1]
        d = State.disks

        # Case 4: All disks have reached the final peg.
        if self.is_goal_old():
            return 0

        # Case 1: The final peg is empty.
        if len(final_peg) == 0:
            return 2 ** (d - 1)

        # Case 2: The final peg contains disks, but not disk d.
        largest_on_final = final_peg[-1]

        if largest_on_final < d:
            c = largest_on_final
            return 2 ** (c - 1) + 2 ** (d - 1)

        # Case 3: Find the largest disk outside the final peg.
        c = 0

        for peg in self.a[:-1]:
            for disk in peg:
                if disk > c:
                    c = disk

        return 2 ** (c - 1)

    def heuristic4a(self):
        # Find the largest disk outside the final peg.
        c = 0

        for peg in self.a[:-1]:
            for disk in peg:
                if disk > c:
                    c = disk

        # All disks have reached the final peg.
        if c == 0:
            return 0

        if c > len(State.k):
            raise ValueError("heuristic4a supports at most 7 disks with the supplied k table")
        return 1 + State.k[c - 1]


def state_key(state):
    return tuple(tuple(peg) for peg in state.a)


def depth_limited_search(state, remaining_depth, path, path_keys=None):
    if path_keys is None:
        path_keys = {state_key(previous) for previous in path}
    if state.is_goal():
        return [], 0
    if remaining_depth == 0:
        return None, 0

    # A state is expanded only when its successors are generated.
    children = state.expand()
    expanded = 1
    for child, action, _ in children:
        key = state_key(child)
        if key in path_keys:
            continue
        path.append(child)
        path_keys.add(key)
        solution, count = depth_limited_search(
            child, remaining_depth - 1, path, path_keys
        )
        path.pop()
        path_keys.remove(key)
        expanded += count
        if solution is not None:
            return [action] + solution, expanded
    return None, expanded


def iterative_deepening_search(start):
    total_expanded = 0
    depth_limit = 0
    while True:
        # This set belongs only to the current path and this iteration.
        solution, expanded = depth_limited_search(start, depth_limit, [start])
        total_expanded += expanded
        if solution is not None:
            return solution, total_expanded
        depth_limit += 1


def ida_star_search(state, g, bound, path, path_keys=None):
    if path_keys is None:
        path_keys = {state_key(previous) for previous in path}
    estimated_total = g + state.h
    if estimated_total > bound:
        return None, estimated_total, 0
    if state.is_goal():
        return [], bound, 0

    children = state.expand()
    expanded = 1
    next_bound = float("inf")
    for child, action, cost in children:
        key = state_key(child)
        if key in path_keys:
            continue
        path.append(child)
        path_keys.add(key)
        solution, child_bound, count = ida_star_search(
            child, g + cost, bound, path, path_keys
        )
        path.pop()
        path_keys.remove(key)
        expanded += count
        if solution is not None:
            return [action] + solution, bound, expanded
        next_bound = min(next_bound, child_bound)
    return None, next_bound, expanded


def iterative_deepening_a_star(start):
    bound = start.h
    total_expanded = 0
    while True:
        solution, next_bound, expanded = ida_star_search(start, 0, bound, [start])
        total_expanded += expanded
        if solution is not None:
            return solution, total_expanded
        if next_bound == float("inf"):
            return None, total_expanded
        bound = next_bound


def solve(disks=4, pegs=3, algorithm="ida", heuristic="3b", goal="original"):
    """Solve one instance. State configuration is shared, so use sequential calls."""
    from types import SimpleNamespace

    if disks < 0 or pegs not in (3, 4):
        raise ValueError("Use a non-negative disk count and 3 or 4 pegs")
    if algorithm not in ("ids", "ida"):
        raise ValueError("algorithm must be 'ids' or 'ida'")
    if goal not in ("original", "empty_ends"):
        raise ValueError("Unknown goal")
    if goal == "empty_ends" and (pegs != 4 or algorithm != "ids"):
        raise ValueError("The empty-ends experiment uses IDS with four pegs")
    if algorithm == "ida" and ((pegs == 3 and heuristic not in ("3a", "3b"))
                               or (pegs == 4 and heuristic != "4a")):
        raise ValueError("Use 3a/3b for three pegs or 4a for four pegs")
    State.goal_name = goal
    State.heuristic_name = heuristic if algorithm == "ida" else "3a"
    start = State.start_state(SimpleNamespace(disks=disks, pegs=pegs))
    try:
        if algorithm == "ids":
            return iterative_deepening_search(start)
        return iterative_deepening_a_star(start)
    finally:
        State.goal_name = "original"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tower of Hanoi: IDS and IDA*")
    parser.add_argument("--disks", type=int, default=4)
    parser.add_argument("--pegs", type=int, choices=[3, 4], default=3)
    parser.add_argument("--algorithm", choices=["ids", "ida"], default="ida")
    parser.add_argument("--heuristic", choices=["3a", "3b", "4a"])
    args = parser.parse_args()
    heuristic = args.heuristic or ("3b" if args.pegs == 3 else "4a")
    solution, expanded = solve(args.disks, args.pegs, args.algorithm, heuristic)
    if solution is None:
        print("No solution found")
    else:
        print("Solution length:", len(solution))
        for action in solution:
            print(" (" + action + ")")
    print("Total expanded states:", expanded)


if __name__ == "__main__":
    main()
