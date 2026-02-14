import logging
import os
import sys
import random

from collections import Counter

from util.constants import *

logger = logging.getLogger(APP_NAME)


# >>>
def handle_assets_path(relative_path: str) -> str:
    logger.info("Util: Converting relative path to absolute path...")

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    absolute_path = os.path.join(base_path, relative_path)
    logger.info("Util: Converted relative path to absolute path for the asset.")

    return absolute_path


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
            # feedback[i] = CORRECT_PLACEMENT_EMOJI
        else:
            secret_remaining.append(s)
            guess_remaining.append(g)
            remaining_indices.append(i)

    secret_counter = Counter(secret_remaining)

    for idx, g in zip(remaining_indices, guess_remaining):
        if secret_counter[g] > 0:
            feedback[idx] = "⚠️"
            # feedback[idx] = WRONG_PLACEMENT_EMOJI
            secret_counter[g] -= 1
        else:
            feedback[idx] = "❌"
            # feedback[idx] = NOT_PRESENT_EMOJI

    logger.info("Util: Evaluted the guess and generated the feedback.")

    return "".join(feedback)


# <<<


# >>>
def create_colour_code():

    logger.info("Util: Creating the colour code...")

    code = [""] * 5

    for i in range(CODE_LENGTH):
        code[i] = random.sample(AVAILABLE_COLOURS, 1)[0]

    logger.info(f"Util: Created the colour code: {code}")

    return code


# <<<
