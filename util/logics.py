import logging
import random
import math

from collections import Counter

from util.constants import *

logger = logging.getLogger(APP_NAME)


# >>>
def create_colour_code(max_attempts=200):

    logger.info(f"Util: Creating the colour code...")

    for attempt in range(max_attempts):
        k = random.choice([2, 3, 4])
        chosen = random.sample(AVAILABLE_COLOURS, k)
        counts = [1] * k
        remaining = 5 - k

        for _ in range(remaining):
            idx = random.randrange(k)
            counts[idx] += 1

        code = []
        for col, cnt in zip(chosen, counts):
            code += [col] * cnt
        random.shuffle(code)

        if not any(cnt > 1 for cnt in counts):
            continue

        if is_trivial(code):
            continue

        ent = calculate_entropy_for_counts(Counter(code).values(), 5)
        logger.info(
            f"Util: Attempt {attempt+1}: Generated code {code} with entropy {ent}"
        )
        if ent < 0.8 or ent > 1.9:
            continue

        logger.info(f"Util: Created the colour code: {code} at attempt {attempt+1}.")
        return code

    code = [""] * 5
    for i in range(CODE_LENGTH):
        code[i] = random.sample(AVAILABLE_COLOURS, 1)[0]

    logger.info(f"Util: Fallback colour code after {max_attempts} attempts: {code}")
    return code


# <<<


# >>>
def calculate_entropy_for_counts(counts, length):

    h = 0.0
    for c in counts:
        p = c / length
        if p > 0:
            h -= p * math.log2(p)
    return h


# <<<


# >>>
def is_trivial(code):
    if len(set(code)) == 1:
        return True

    if code == list(reversed(code)):
        return True

    run = 1
    for i in range(1, 5):
        if code[i] == code[i - 1]:
            run += 1
            if run >= 4:
                return True
        else:
            run = 1
    return False


# <<<


# >>>
def evaluate_guess(secret, guess):

    logger.info("Util: Evaluating the guess against the secret code...")

    feedback = [""] * 5

    secret_remaining = []
    guess_remaining = []
    remaining_indices = []

    for i, (s, g) in enumerate(zip(secret, guess)):
        if s == g:
            feedback[i] = "✅"
        else:
            secret_remaining.append(s)
            guess_remaining.append(g)
            remaining_indices.append(i)

    secret_counter = Counter(secret_remaining)

    for idx, g in zip(remaining_indices, guess_remaining):
        if secret_counter[g] > 0:
            feedback[idx] = "⚠️"
            secret_counter[g] -= 1
        else:
            feedback[idx] = "❌"

    logger.info("Util: Evaluted the guess and generated the feedback.")

    return "".join(feedback)


# <<<


# >>>
def convert_feedback_emojis_to_string(feedback):

    converted_feedback = (
        feedback.replace("✅", "Y").replace("⚠️", "M").replace("❌", "N")
    )
    logger.info(
        f"Util: Converted feedback emojis to string format: {feedback} to {converted_feedback}"
    )
    return converted_feedback


# <<<
