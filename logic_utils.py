def get_range_for_difficulty(difficulty: str) -> tuple:
    """Return the numeric range for a given difficulty level.

    Maps a difficulty string to a (low, high) inclusive integer range
    that defines the pool of possible secret numbers for the game.

    Args:
        difficulty (str): One of "Easy", "Normal", or "Hard".

    Returns:
        tuple: A (low, high) pair of integers representing the inclusive
               range. Defaults to (1, 100) for unrecognised values.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple:
    """Parse raw text input from the player into a validated integer guess.

    Accepts whole numbers and decimals (decimals are truncated to int).
    Returns a three-element tuple so the caller can handle errors without
    raising exceptions.

    Args:
        raw (str): The raw string entered by the player in the text input.

    Returns:
        tuple: A three-element tuple (ok, guess_int, error_message) where:
               - ok (bool): True if parsing succeeded, False otherwise.
               - guess_int (int | None): The parsed integer, or None on failure.
               - error_message (str | None): A human-readable error string,
                 or None if parsing succeeded.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
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


def check_guess(guess: int, secret: int) -> str:
    """Compare the player's guess to the secret number and return the outcome.

    Both arguments must be integers so that comparison is always numeric.
    This avoids the lexicographic ordering bug that occurs when either
    value is a string (e.g. "5" > "42" evaluates to True in Python).

    Args:
        guess (int): The number submitted by the player.
        secret (int): The target number the player is trying to guess.

    Returns:
        str: One of three outcome strings:
             - "Win"      if guess equals secret.
             - "Too High" if guess is greater than secret.
             - "Too Low"  if guess is less than secret.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
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


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the latest guess outcome.

    Winning awards points that decrease with each additional attempt.
    A "Too High" guess on an even attempt number gives a small bonus;
    on an odd attempt it applies a small penalty. A "Too Low" guess
    always applies a small penalty.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): The result of the guess — "Win", "Too High", or "Too Low".
        attempt_number (int): The 1-based number of the current attempt.

    Returns:
        int: The updated score after applying the outcome's point change.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(50, "Too Low", 3)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score