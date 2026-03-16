def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py into logic_utils.py
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
    Compare guess to secret and return outcome string.

    outcome: "Win", "Too High", or "Too Low"
    """
    # FIXME was: suspected the hint labels "Go Higher" / "Go Lower" were
    # swapped inside this function.
    # FIX: The labels here were never the problem. The real bug was in app.py
    # where secret was cast to str on even attempts, causing lexicographic
    # string comparison to flip Too High / Too Low unpredictably.
    # This function now always receives and compares plain ints.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
