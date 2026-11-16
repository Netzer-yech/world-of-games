# World of Games (WoG)

A collection of small console games in Python, built in phases as the final project of a DevOps course.
Later phases add a score system, a web service, Docker, a Jenkins CI/CD pipeline and deployment.


## Status

Last updated: 29.10.26

- **Part 1 (Foundations):** done. All 14 tasks are complete and merged into `main`.
- **Automated tests:** in progress on the `feature/test-suite` branch, using pytest.
- **Next:** Part 2, waiting for the brief.


## Repo structure

```text
world-of-games/
├── MainGame.py              # Entry point: asks the player's name, prints the welcome, opens the menu
├── Live.py                  # welcome(), the game menu, and get_number() for validated number input
├── GuessGame.py             # Guess Game: guess a secret number from 1 to the difficulty
├── MemoryGame.py            # Memory Game: a number sequence shows for 0.7 seconds, repeat it back
├── CurrencyRouletteGame.py  # Currency Roulette: guess the ILS value of a random USD amount (live API)
├── requirements.txt         # Packages the game needs to run (requests, pinned)
├── .gitignore               # Files git must not track (venv, caches, secrets)
└── README.md                # This file
```


## How to run

Requirements: Python 3 (developed with 3.14) on Linux or WSL, and internet access for Currency Roulette.

Run these from the repo root. Create the venv once, and activate it in every new terminal.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python MainGame.py
```


## Game flow

1. `MainGame.py` asks for the player's name and prints the welcome from `Live.welcome()`.
2. `Live.load_game()` shows the menu and asks for a game (1-3) and a difficulty (1-5). Invalid input gets a message and a new prompt.
3. `load_game()` calls the chosen game's `play(difficulty)`.
4. Every `play()` returns `True` (won) or `False` (lost), and `load_game()` prints the result.

What difficulty changes in each game:

| Game | Difficulty controls |
|---|---|
| Guess Game | The secret number is from 1 to the difficulty |
| Memory Game | How many numbers (1-101) the sequence has |
| Currency Roulette | The winning margin: the exact ILS value plus or minus (5 - difficulty) |

If the currency API fails, the Currency Roulette round is cancelled and counts as a loss.


## Conventions and decisions

### Git

- One branch per change, named by type: `feature/...`, `docs/...`, `fix/...`. Merged into `main` through a pull request, then deleted.
- One commit per completed file. Unfinished work that must be saved is committed with a `WIP:` prefix.

### Code

- Input is read in small, separate functions; the game logic only receives values. This keeps the logic testable.
- Every game's `play(difficulty)` returns `True` or `False`.
- Money uses `Decimal`, rounded to 2 places (`ROUND_HALF_UP`). The winning interval includes both edges.
- The currency rate comes from `https://open.er-api.com/v6/latest/USD` (free, no key), with a 5-second timeout. Any failure returns `None`, and the round is cancelled.
- Packages are installed in a venv, never with `sudo pip`. Versions are pinned in `requirements.txt`.

### For AI assistants

- This is a learning project: the owner writes all the code by hand. Explain, review and point out mistakes; do not write or edit files.
- Read the Status section first, and do not start work from a later phase.