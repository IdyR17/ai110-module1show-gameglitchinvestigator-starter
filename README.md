# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose:** A number guessing game built with Streamlit. The player picks a difficulty, then tries to guess a secret number within a limited number of attempts, using "Go Higher / Go Lower" hints. Fewer guesses earn a higher score.

**Bugs found:**

- Hint messages were swapped ("Go HIGHER" when the guess was too high).
- On every even attempt the secret was converted to a string, so numbers were compared alphabetically (`"9" > "50"`). A `try/except` hid the error.
- "Hard" had a smaller range than "Normal", and the prompt always said "1 to 100".
- "New Game" didn't reset `status` or `history`, so you couldn't play again after winning or losing.
- Attempts started at 1, so the player got one fewer guess than promised.

**Fixes applied:**

- Moved the game logic into `logic_utils.py` and imported it into `app.py`.
- Swapped the hint messages and removed the `try/except`; the secret is always passed as an `int`.
- Changed ranges to Easy 1–20, Normal 1–50, Hard 1–100, and made the prompt show the current range.
- "New Game" now resets the secret (using the difficulty's range), attempts, status, and history.
- Added pytest tests for the hints, the string-comparison bug, and the difficulty ranges.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and the game opens in the browser.
2. Pick a difficulty in the sidebar. The sidebar and the prompt show the matching range (e.g. Normal: 1 to 50) and number of attempts.
3. Open "Developer Debug Info" to see the secret number (e.g. 32).
4. Guess a number above the secret (e.g. 45) and click **Submit Guess**. The hint says "Go LOWER" and attempts left drops by one.
5. Guess a number below the secret (e.g. 9). The hint says "Go HIGHER", correctly, every turn.
6. Guess the secret (32). Balloons appear and the game shows "You won!" with the final score.
7. Click **New Game**. A new secret is picked within the current difficulty's range, and you can play again right away.

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 33%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 44%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 55%]
tests/test_game_logic.py::test_single_digit_guess_compared_as_number PASSED [ 66%]
tests/test_game_logic.py::test_hard_range_is_bigger_than_normal PASSED   [ 77%]
tests/test_game_logic.py::test_wrong_guess_never_adds_points PASSED      [ 88%]
tests/test_game_logic.py::test_first_try_win_scores_100 PASSED           [100%]

============================== 9 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
