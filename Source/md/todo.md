# Todos

- [x] export `requirements.txt`
- [x] map level indexing

## Assessment

- [x] Implement BFS correctly.
- [x] Implement DFS correctly.
- [x] Implement UCS correctly.
- [x] Implement A\* correctly.
- [x] Generate at least 10 test cases for each level with different attributes.
- [x] GUI.
- [x] Output files.
- [x] Videos to demonstrate all algorithms for some test cases.
- [x] Report your algorithm and experiment with some reflection or comments.
- [x] Implement Swarm Algorithm, Convergent Swarm Algorithm, or Bidirectional Swarm Algorithm.
- [x] Write report for Swarm Algorithm, Convergent Swarm Algorithm, or Bidirectional Swarm Algorithm.

## Algo

- [x] use hashing for visited state (called `tranposition table`) => using frozenset() instead of set() because of hassable problem
- [x] deadlock detection (simple/count area/freeze/...) => freeze deadlock
- [x] assignment problem => hungarian matching
- [ ] restart searching to prevent stucking

## GUI

- [x] gameplay design
- [x] visualize grid item
- [x] game interaction
- [x] toolbar (play, pause, reset, speed up/down, undo/redo move)
- [x] select algo
- [x] select map
- [x] settings (mute/unmute bgm, window resolution)
- [x] display fps, step count, weight pushed, elapsed time
- [x] movement history
- [x] simulate movement
- [x] window can be freely resized
- [x] minimap with zoom in/out + moving screen
- [x] change speed of simulation
- [x] import new map (auto-generate output file for gui to work with)
- [x] bgms controller
- [ ] change app icon + custom caption with algo and map info
- [ ] sound effect for victory, movement and click action
- [ ] undo/redo movement handle

## Report

- [x] Member information (Student ID, full name, etc.)
- [x] task assignment info (with assigned to, completion rate)
- [x] self-evaluation of the project requirements
- [x] each algo report (detailed explanation including imple process, heuristic functin, etc.) with imgs and diagrams
- [x] test case description and experiment results (mem usage, time complexity, etc.) (Highlight challenges and compare the overall behavior of your algorithms.) (use tables)
- benchmark using chart and graphs (with/without opt like deadlock, hungarian) => using `matplotlib.pyplot`
  - [x] mem
  - [x] time
  - [x] state
