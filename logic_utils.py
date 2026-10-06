def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    # FIX: Hard was 1-50 (easier than Normal's 1-100). I noticed it; Claude suggested making Hard 1-200,
    # but I swapped the two ranges instead (Normal 1-50, Hard 1-100).
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Hints were backwards. Claude moved this from app.py, swapped the messages, and removed the
    # try/except TypeError that hid the string-comparison bug. Verified with pytest and the live app.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Win bonus was off by one. Claude corrected the formula; test_first_try_win_scores_100 checks it.
        # attempt_number is 1 on the first guess, so a first-try win is worth 100
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: A "Too High" guess on even attempts gave +5. Claude flagged it in its first code review; Claude made every miss -5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
