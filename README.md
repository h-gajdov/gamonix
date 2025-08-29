# Gamonix

Gamonix is a backgammon AI built as a faculty project for an Artificial Inteligence course.

It is built aroung an expectimax algorithm with caching, beam search and search optimizations, as well as custom heuristics that evaluate each board state.

The engine has a GUI built with the Pygame graphics library.

## Installation

To install the project locally:

1. **Clone the repository**:

```bash
git clone https://github.com/h-gajdov/gamonix.git
cd gamonix
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run the GUI**:

```bash
PYTHONPATH=. py ui/game.py
```

## Changing agents for GUI

You can choose which **AI agent** to play against by running the GUI with the `--agent` parameter:

```bash
PYTHONPATH=. py ui/game.py --agent <agent_name>
```

### Available Agents

- Random - random
- Greedy Agents
  - Shallow greedy - shallow_greedy
  - Depth greedy - depth_greedy
- Expectimax Agents
  - Standard - expectimax\_{max_depth}d
    (example: expectimax_2d)
  - With caching - caching_expectimax\_{max_depth}d
- Beam Expectimax Agents
  - Fixed beam width - beam_expectimax\_{max_depth}d\_{beam_width}b
    (example: beam_expectimax_2d_5b)
  - Adaptive beam - adaptive_beam\_{max_depth}d\_{beam_width}b

Example of running the command with `--agent`:

```bash
PYTHONPATH=. py ui/game.py --agent beam_expectimax_2d_5b
```

## Evaluating agents

You can test how different agents perform against each other using the console interface:

```bash
PYTHONPATH=. py ui/console.py -s --agents <first_agent_name> <second_agent_name> --games <n>
```

- `--agents <first_agent_name> <second_agent_name>` <br/>
  Specify the two agents to compete (see [Available Agents](#available-agents)).

- `--games` (optional) <br/>
  Number of games to simulate. If omitted, defaults to 100 games.

- `-s` (optional) <br/>
  Saves results to `/results/agent_evaluation`. Without this flag, results are printed only in the console

Example. Run 200 games between a depth-based greedy agent and an expectimax agent with depth 2, and save the results:

```bash
PYTHONPATH=. py ui/console.py -s --agents depth_greedy expectimax_2d --games 10
```

## Playing against gnubg

You can test the performance of the AI agents against gnubg.

### 1. Install gnubg CLI

Download the gnubg CLI version from this [link](https://www.gnu.org/software/gnubg/#downloading).

### 2. Configure gnubg

Open the GNU Backgammon app and in Settings -> Options you need to disable "use doubling cube" in the Cube tab, set dice to "manual dice" in the Dice tab and before running the script in the New panel you should press "Modify player settings..." and set Player 0 to be GNU Backgammon and set its difficulty.

Next in the main directory of this project you should create a `.env` file where you define:

```env
PATH_TO_GNUBG=D:\<path-to-gnubg>\gnubg\gnubg-cli
```

### 3. Run an agent vs gnubg

Use the following command:

```bash
PYTHONPATH=. py ui/play_against_gnu.py -s --agent <agent_name>
```

- `--agent <agent_name>` <br/>
  Specify the agent that will play against gnubg (see [Available Agents](#available-agents)).

- `-s` (optional) <br/>
  Saves results to `/results` in folders named agent_name_vs_gnubg. Without this flag, the game is printed only in the console

Example. Run expectimax_2d against gnubg and save the results:

```bash
PYTHONPATH=. py ui/play_against_gnu.py -s --agent expectimax_2d
```
