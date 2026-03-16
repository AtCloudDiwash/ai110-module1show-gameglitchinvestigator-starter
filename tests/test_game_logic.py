from logic_utils import check_guess, parse_guess

# ── Baseline tests ────────────────────────────────────────────────────────────

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ── Bug 1 regression: hint direction was flipped on even attempts ─────────────
# Root cause: app.py cast secret to str on even attempts, making Python use
# lexicographic comparison which reversed Too High / Too Low in many cases.

def test_bug1_low_guess_not_reported_too_high():
    # "5" > "42" is True lexicographically, so old code wrongly said Too High.
    result = check_guess(5, 42)
    assert result == "Too Low"

def test_bug1_high_guess_not_reported_too_low():
    # "80" < "9" is True lexicographically, so old code wrongly said Too Low.
    result = check_guess(80, 9)
    assert result == "Too High"

def test_bug1_check_guess_always_uses_int_comparison():
    # Exhaustive spot-check: guess below secret must always be Too Low.
    for guess, secret in [(1, 100), (10, 11), (49, 50), (3, 30)]:
        assert check_guess(guess, secret) == "Too Low"
    # And guess above secret must always be Too High.
    for guess, secret in [(100, 1), (11, 10), (51, 50), (30, 3)]:
        assert check_guess(guess, secret) == "Too High"


# ── Bug 2 regression: new game did not reset all state ────────────────────────
# Root cause: only attempts and secret were reset; score, status, and history
# carried over from the previous game.

def simulate_new_game(current_state: dict, new_secret: int) -> dict:
    """Mirrors the fixed new_game block in app.py."""
    return {
        "attempts": 0,
        "secret": new_secret,
        "score": 0,
        "status": "playing",
        "history": [],
    }

def test_bug2_score_resets_to_zero():
    state = {"attempts": 5, "secret": 42, "score": 75, "status": "won", "history": [10, 20, 42]}
    new_state = simulate_new_game(state, new_secret=7)
    assert new_state["score"] == 0

def test_bug2_status_resets_to_playing():
    state = {"attempts": 5, "secret": 42, "score": 75, "status": "won", "history": [10, 20, 42]}
    new_state = simulate_new_game(state, new_secret=7)
    assert new_state["status"] == "playing"

def test_bug2_history_clears():
    state = {"attempts": 5, "secret": 42, "score": 75, "status": "won", "history": [10, 20, 42]}
    new_state = simulate_new_game(state, new_secret=7)
    assert new_state["history"] == []

def test_bug2_attempts_resets_to_zero():
    state = {"attempts": 5, "secret": 42, "score": 75, "status": "won", "history": [10, 20, 42]}
    new_state = simulate_new_game(state, new_secret=7)
    assert new_state["attempts"] == 0


# ── Bug 3 regression: guess history was delayed by one submit ─────────────────
# Root cause: history.append() ran after the history display widget had already
# rendered (Streamlit renders top-to-bottom). The fix adds st.rerun() so the
# next render sees the updated history immediately.
# The unit test verifies the append logic itself is correct and immediate.

def simulate_submit(history: list, raw: str) -> list:
    """Mirrors the fixed submit block: parse then append to history."""
    ok, guess_int, _ = parse_guess(raw)
    updated = list(history)
    if ok:
        updated.append(guess_int)
    else:
        updated.append(raw)
    return updated

def test_bug3_guess_appended_on_submit():
    history = []
    history = simulate_submit(history, "25")
    assert 25 in history

def test_bug3_multiple_guesses_all_logged():
    history = []
    for guess in ["10", "30", "50"]:
        history = simulate_submit(history, guess)
    assert history == [10, 30, 50]

def test_bug3_invalid_guess_still_logged():
    # Invalid input should also be recorded (as the raw string).
    history = []
    history = simulate_submit(history, "abc")
    assert "abc" in history
