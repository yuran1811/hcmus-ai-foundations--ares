# Todos

- [x] export `requirements.txt`
- [ ] map level indexing
- [ ] generate outputs

## Assessment

- [x] Implement BFS correctly.
- [x] Implement DFS correctly.
- [x] Implement UCS correctly.
- [x] Implement A\* correctly.
- [x] Generate at least 10 test cases for each level with different attributes.
- [x] GUI.
- [ ] Output files.
- [ ] Videos to demonstrate all algorithms for some test cases.
- [ ] Report your algorithm and experiment with some reflection or comments.
- [ ] Implement Swarm Algorithm, Convergent Swarm Algorithm, or Bidirectional Swarm Algorithm.
- [ ] Write report for Swarm Algorithm, Convergent Swarm Algorithm, or Bidirectional Swarm Algorithm.

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
- [ ] change app icon + custom caption with algo and map info
- [ ] import new map (auto-generate output file for gui to work with)
- [ ] list of bgms
- [ ] sound effect for victory, movement and click action
- [ ] undo/redo movement handle

## Report

- [ ] each algo report (detailed explanation including imple process, heuristic functin, etc.) with imgs and diagrams
- [ ] task assignment info
- [ ] self-evaluation of the project requirements
- [ ] test case description and experiment results (mem usage, time complexity, etc.) (use tables)
- benchmark using chart and graphs (with/without opt like deadlock, hungarian) => using `matplotlib.pyplot`
  - [ ] mem
  - [ ] time
  - [ ] state
