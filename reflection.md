# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it looked fine: a title, a sidebar with difficulty settings, a text box, and Submit/New Game buttons. Once I started guessing, the hints didn't make sense as confirmed by debug window. When my guess was too high it told me to "Go HIGHER," and the hints seemed to change randomly between guesses even when my guess logic was consistent. I also noticed the game always said "Guess a number between 1 and 100" no matter which difficulty I picked, and that "Hard" actually had a smaller range (1–50) than "Normal" (1–100). Also, after winning or losing, clicking "New Game" didn't actually let me play again.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                                              | Expected Behavior               | Actual Behavior                                                                                                         | Console Output / Error                                   |
| -------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Secret = 50, guess `80`                            | Hint says "Go LOWER"            | Hint says "Go HIGHER!" (hint messages are swapped in `check_guess`)                                                     | logic bug, no error                                      |
| Secret = 50, guess `9` on an even-numbered attempt | Hint says "Go HIGHER"           | Says "Too High" because on even attempts the secret is turned into a string, so `"9" > "50"` is compared alphabetically | None, the `TypeError` is caught silently by `try/except` |
| Win a game, then click "New Game"                  | Fresh game starts               | Still shows "You already won" because `status` is never reset to `"playing"`; history isn't cleared either              | None                                                     |
| Select "Hard" difficulty                           | Bigger range / harder game      | Range is 1–50, easier than Normal (1–100); info text still says "1 and 100"                                             | None                                                     |
| Normal mode (8 attempts), fresh game               | "Attempts left: 8"              | Shows 7 because `attempts` starts at 1 instead of 0                                                                     | None                                                     |
| Type `abc` and submit                              | Error message, attempt not used | Error shown but it still uses up an attempt                                                                             | None                                                     |
| Switch difficulty from Normal to Easy              | New secret within 1–20          | Secret stays from the old range (e.g. 87), so it's impossible to win                                                    | None                                                     |

Other things I noticed: "New Game" picks the secret from 1–100 regardless of difficulty, and `update_score` gives +5 points for a "Too High" guess on even attempts.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? I used Claude Code inside VS Code.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  I asked Claude why the hints felt wrong, and it found two bugs working together. The "Go HIGHER" and "Go LOWER" messages in check_guess were swapped. Also, on every even attempt the code turned the secret into a string, so Python compared "9" and "50" alphabetically and said 9 was "Too High." A try/except TypeError hid that second bug. Claude moved check_guess into logic_utils.py, swapped the messages, removed the try/except, and changed app.py to always pass the secret as an int. To verify it, I ran pytest and all the tests passed, including a new one checking that 9 against 50 is "Too Low." I also played the game with the debug panel open: guessing above the secret said "Go LOWER," and guessing below it said "Go HIGHER."
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  Claude suggested fixing the difficulty bug by making Hard's range 1–200 and leaving Normal at 1–100. I didn't accept that as written. Instead I swapped the ranges, so Normal is 1–50 and Hard is 1–100, because I wanted Hard to feel like the original game's 1–100, with Easy and Normal as easier steps below it. To verify my version, I ran pytest and all 9 tests passed, including the one that checks Hard's range is bigger than Normal's. I also switched between all three difficulties in the app and checked that the prompt showed the right range (1–20, 1–50, 1–100)

---

## 3. Debugging and testing your fixes

I counted a bug as fixed only when two things were true: an automated test for it passed, and the game behaved correctly when I played it myself. For the manual check, I ran python -m streamlit run app.py, opened the Developer Debug Info panel to see the secret, and guessed above and below it. Guessing above now said "Go LOWER" and guessing below said "Go HIGHER," every turn and not just every other one. I also checked that New Game worked after winning, and that switching difficulty showed the right range. With pytest, the most useful test was guessing 9 against a secret of 50. It should be "Too Low," but the old code said "Too High" because it compared "9" and "50" as text, so this test showed me the bug was really about data types, not just swapped messages. Claude wrote the new tests and explained that the starter tests would fail because check_guess returns two values (the outcome and the message), so they had to unpack the result.

---

## 4. What did you learn about Streamlit and state?

Every time you do anything in a Streamlit app, like clicking a button, typing in a box, or changing a dropdown, Streamlit runs your whole Python script again from the top. That's a "rerun." A normal variable is created fresh on each rerun, so if the game said secret = random.randint(1, 100) at the top, you'd get a new secret number every time you clicked Submit.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  I want to keep using the two-part check: a bug only counts as fixed when a pytest test passes _and_ the app behaves correctly when I use it myself. Writing the bug reproduction log first (input, expected, actual) also made it much easier to explain problems to Claude and to know exactly what to test afterward.

- What is one thing you would do differently next time you work with AI on a coding task?
  I would ask the AI to explain the cause of a bug before letting it change any code, and review each change before accepting it. The difficulty fix showed me the AI's first suggestion isn't always the one that fits what I want.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project showed me that AI-generated code can look clean and even claim to be "production-ready" while hiding real bugs. Now I treat AI code as a first draft that I need to read, test, and question, not something to trust automatically.
