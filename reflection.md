# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

### Bug 1: Hints show the wrong direction

Expected Behavior:
When the player submits a guess that is lower than the correct number, the game should display a hint saying "Go Higher". If the guess is higher than the correct number, it should say "Go Lower".

Actual Behavior:
The hint system gives the opposite response. When the guess is lower than the correct number, the game tells the player to "Go Lower". When the guess is higher than the correct number, it tells the player to "Go Higher". The hint logic appears to be reversed.

---

### Bug 2: "Start New Game" does not fully reset the game state

Expected Behavior:
When "Start New Game" is clicked, the game should completely reset all game data. This includes generating a new target number, clearing previous guesses, resetting attempts, clearing hints, and starting a fresh game.

Actual Behavior:
When the "Start New Game" button is pressed, some values such as attempts are reset, but other parts of the game state remain unchanged. This causes the new game to still contain information from the previous round.

---

### Bug 3: Guess history is not logged at the correct time

Expected Behavior:
Each time the player enters a number and presses "Submit", that guess should immediately be recorded in the game history.

Actual Behavior:
The guess is not logged when the player presses "Submit". Instead, it only appears after another guess is entered and submitted. This causes the history log to be delayed and inaccurate.

---

## 2. How did you use AI as a teammate?

I used Claude Code and ChatGPT together throughout this project. Claude Code handled most of the code edits and refactoring directly in the files, while ChatGPT was used to talk through ideas and get a second opinion on what certain bugs might be.

**Correct AI suggestion — Bug 1 root cause:**
I originally suspected that the hint labels inside `check_guess` were swapped — that the function itself was returning the wrong direction. The AI pointed out that `check_guess` was actually correct, and the real problem was elsewhere in `app.py` where the secret number was being cast to a string on every even-numbered attempt. This caused Python to compare numbers alphabetically instead of numerically, which flipped the hint results in certain cases. I verified this by writing two targeted pytest cases that specifically tested guesses where string and numeric ordering disagree, and both tests passed after the fix.

**Incorrect/misleading AI suggestion — Bug 3 fix broke win condition and hints:**
When fixing the history delay bug, the AI suggested adding `st.rerun()` at the end of the submit block to force the page to refresh immediately after a guess. The suggestion was misleading because `st.rerun()` was placed unconditionally, meaning it also fired when the player guessed correctly or ran out of attempts. This caused the win animation (balloons) and the success message to never appear since the page reloaded before they could render. The same rerun also wiped the hint warning before it displayed. I caught both issues by manually playing the game — there were no balloons on a correct guess and no hints after any guess. Two follow-up fixes were needed: restricting `st.rerun()` to only in-progress guesses, and storing the hint in session state so it survived the rerun.

---

## 3. Debugging and testing your fixes

I used three steps to decide whether a bug was really fixed. First, I reviewed every change the AI made by reading through the diff and checking that each `#FIXME` and `#FIX` comment was placed correctly and actually described the real problem — this caught cases where the AI's fix introduced new issues, like `st.rerun()` breaking the win screen and hints. Second, I manually played the game after each fix to confirm the behavior matched the expected behavior described in Phase 1 — I checked that hints pointed in the right direction, that a new game wiped all previous state, and that guess history appeared immediately. Third, I ran the full pytest suite (`python3 -m pytest tests/ -v`) which covered all three bugs with 13 tests total and confirmed every case passed.

The most useful test was `test_bug1_low_guess_not_reported_too_high`, which checked that a guess of `5` against a secret of `42` returns `"Too Low"`. This specific case would have silently failed with the original code because Python's string comparison makes `"5" > "42"` evaluate to `True`, flipping the result to `"Too High"`. Running this test made the bug concrete and measurable rather than something I could only catch by luck during manual play.

The AI helped write all the pytest cases. I instructed it to write tests targeting each specific bug, and it generated the `simulate_new_game` and `simulate_submit` helper functions to test Bug 2 and Bug 3 logic without needing Streamlit running. I then reviewed each test to make sure it was actually testing the right thing before accepting it.

---

## 4. What did you learn about Streamlit and state?

In Streamlit, the whole script runs again from the beginning whenever a user clicks a button or types something. Because of this, normal variables get reset every time the script runs again. To keep important values between these reruns, Streamlit provides session state, which stores data for the user’s session. It works like a small storage space where values stay saved even when the script reruns.If you want something like hints, messages, or user progress to stay visible after an interaction, you should store it in session state. Otherwise, the value will disappear when the script runs again.

---

## 5. Looking ahead: your developer habits

One strategy I want to reuse is giving the AI full context by sharing multiple related files and explaining the overall situation before asking a question. This helps the AI understand the project better and give more accurate suggestions.

Next time, before accepting AI-generated changes, I will think about how the change might affect other parts of the code. Previously, a change fixed one issue but broke the win condition logic and the hint feature.

This project showed me that AI-generated code can be very helpful, but it must be reviewed carefully. AI may fix one function but miss how that change affects other dependent parts of the code.
