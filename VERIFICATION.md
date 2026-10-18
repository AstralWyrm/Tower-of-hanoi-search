# Verification record

Verified on 2026-10-18 with Python 3.12.14.

- `python -m unittest discover -s tests -v`: 4 tests passed.
- Every notebook code cell was executed successfully; all outputs are saved.
- All Python sources parse successfully.
- Core CLI entry points run with `python -S`, without site packages.
- Full experiments executed, including h3b with six disks, k(6), and h4a with seven disks.
- All 20 stored move sequences were replayed to check move legality and goal states.
- Large-case expanded counts reproduced: 8,033,606 / 2,115,456 / 9,176,981.
- Small-state heuristic bounds were checked against independent BFS distances.
