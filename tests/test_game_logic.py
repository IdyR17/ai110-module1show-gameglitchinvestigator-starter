from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug fix: a guess above the secret used to tell the player to go HIGHER
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: a guess below the secret used to tell the player to go LOWER
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_single_digit_guess_compared_as_number():
    # Bug fix: the secret was sometimes a string, so "9" > "50" was True
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_hard_range_is_bigger_than_normal():
    # Bug fix: Hard used to be 1-50, which is easier than Normal (1-100)
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high

def test_wrong_guess_never_adds_points():
    # Bug fix: a "Too High" guess on an even attempt used to give +5
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too Low", 2) == -5

def test_first_try_win_scores_100():
    # Bug fix: the win bonus was off by one attempt
    assert update_score(0, "Win", 1) == 100
