import random
import logging

from collections import Counter

from util.constants import *


logger = logging.getLogger(APP_NAME)


# >>>
class SystemDecoder:

    def __init__(self):

        self.turn = 0
        self.current_guess = []

        self.present_colours = set()
        self.eliminated_colours = set()
        self.completed_colours = set()

        self.correct_positions = dict()
        self.forbidden_positions = dict()

        self.colour_counts = Counter()
        self.unused_colours = AVAILABLE_COLOURS.copy()
        self.discovery_mode = True
        self.discovery_guess_count = 0
        self.placement_guess_count = 0
        logger.info("Util: SystemDecoder initialized.")

    # -----------------------------------------------------
    # GENERATE GUESS
    # -----------------------------------------------------
    def generate_guess(self):

        self.turn = self.turn + 1

        if self.turn == 1:
            self.current_guess = random.sample(AVAILABLE_COLOURS, 5)
            logger.info(f"Util: SystemDecoder guess: {self.current_guess}.")
            return self.current_guess

        if self.discovery_mode == True and len(self.present_colours) < 5:
            self.current_guess = self.discovery_guess()
            logger.info(f"Util: SystemDecoder guess: {self.current_guess}.")
            return self.current_guess

        self.current_guess = self.placement_guess()
        logger.info(f"Util: SystemDecoder guess: {self.current_guess}.")
        return self.current_guess

    # -----------------------------------------------------
    # DISCOVERY PHASE
    # -----------------------------------------------------
    def discovery_guess(self):

        self.discovery_guess_count += 1
        new_guess = [None] * 5

        for idx, colour in self.correct_positions.items():
            new_guess[idx] = colour

        remaining_slots = {i for i, c in enumerate(new_guess) if c is None}

        for colour, indices in self.forbidden_positions.items():

            if colour in self.completed_colours:
                continue

            if colour in self.correct_positions.values():
                continue

            forbidden_slots = set(map(int, indices))
            available_slots = list(remaining_slots - forbidden_slots)
            if not available_slots:
                continue
            new_idx = random.choice(available_slots)
            new_guess[new_idx] = colour
            remaining_slots.remove(new_idx)

        for idx in list(remaining_slots):

            present_colours = list(self.present_colours)

            if self.unused_colours:
                colour = random.choice(list(self.unused_colours))
                new_guess[idx] = colour
                self.unused_colours.remove(colour)
            elif present_colours:
                while True:
                    colour = random.choice(present_colours)

                    if (
                        colour in self.forbidden_positions
                        and str(idx) in self.forbidden_positions[colour]
                    ):
                        present_colours.remove(colour)
                        continue

                    new_guess[idx] = colour
                    break

            else:
                new_guess[idx] = random.choice(new_guess[:4])

        return new_guess

    # -----------------------------------------------------
    # PLACEMENT PHASE
    # -----------------------------------------------------
    def placement_guess(self):

        self.placement_guess_count += 1
        new_guess = [None] * 5

        if len(self.present_colours) == 1:
            new_guess = [list(self.present_colours)[0]] * 5
            return new_guess

        for idx, colour in self.correct_positions.items():
            new_guess[idx] = colour

        remaining_slots = {i for i in range(5) if new_guess[i] is None}

        if len(self.present_colours) == 2:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours:
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots
                if not allowed_slots:
                    continue

                for idx in allowed_slots:
                    new_guess[idx] = colour

                remaining_slots = remaining_slots - allowed_slots

            if remaining_slots:

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in self.present_colours
                }

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

        if len(self.present_colours) == 3:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours:
                    continue

                correct_colour_counts = Counter(self.correct_positions.values())
                if (
                    colour in self.correct_positions.values()
                    and correct_colour_counts[colour] == self.colour_counts[colour]
                ):
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots
                if not allowed_slots:
                    continue

                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)

            if remaining_slots:

                for idx in remaining_slots:

                    candidate_colours = [
                        c
                        for c in self.present_colours
                        if c not in self.completed_colours
                    ]

                    for colour, indices in self.forbidden_positions.items():
                        if colour in candidate_colours:
                            forbidden_slots = set(map(int, indices))
                            if idx in forbidden_slots:
                                candidate_colours.remove(colour)

                    if not candidate_colours:
                        candidate_colours = list(self.present_colours)

                    forbidden_counts = {
                        colour: len(self.forbidden_positions.get(colour, []))
                        for colour in candidate_colours
                    }

                    preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                    new_guess[idx] = preferred_colour

        if len(self.present_colours) == 4:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours and self.placement_guess_count > 1:
                    continue

                if colour in self.correct_positions.values():
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots
                if not allowed_slots:
                    continue

                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)

            if remaining_slots:

                candidate_colours = [
                    c for c in self.present_colours if c not in self.completed_colours
                ]

                for colour, indices in self.forbidden_positions.items():
                    if colour in candidate_colours:
                        forbidden_slots = set(map(int, indices))
                        if any(idx in forbidden_slots for idx in remaining_slots):
                            candidate_colours.remove(colour)

                if not candidate_colours:
                    candidate_colours = list(self.present_colours)

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in candidate_colours
                }

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                double_count_colour = None
                for colour in candidate_colours:
                    if self.colour_counts.get(colour, 0) > 1:
                        double_count_colour = colour
                        break
                if double_count_colour != None:
                    preferred_colour = double_count_colour

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

        if len(self.present_colours) == 5:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours:
                    continue

                if colour in self.correct_positions.values():
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots
                if not allowed_slots:
                    continue

                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)

            if remaining_slots:

                candidate_colours = [
                    c for c in self.present_colours if c not in self.completed_colours
                ]
                if not candidate_colours:
                    candidate_colours = list(self.present_colours)

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in candidate_colours
                }

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

        return new_guess

    # -----------------------------------------------------
    # UPDATE KNOWLEDGE
    # -----------------------------------------------------
    def update_knowledge(self, feedback):

        colour_feedback_count = Counter()

        for i, (colour, fb) in enumerate(zip(self.current_guess, feedback)):
            if fb == CORRECT:
                self.present_colours.add(colour)
                self.correct_positions[i] = colour
                colour_feedback_count[colour] += 1

        for i, (colour, fb) in enumerate(zip(self.current_guess, feedback)):
            if fb == MISTAKE:
                self.present_colours.add(colour)

                if colour in self.forbidden_positions:
                    self.forbidden_positions[colour].add(i)
                else:
                    self.forbidden_positions[colour] = {i}

                colour_feedback_count[colour] += 1

        for i, (colour, fb) in enumerate(zip(self.current_guess, feedback)):
            if fb == WRONG:
                if colour not in self.present_colours:
                    self.eliminated_colours.add(colour)

                if colour in self.present_colours:
                    correct_colour_counts = Counter(self.correct_positions.values())
                    if (
                        colour in self.correct_positions.values()
                        and correct_colour_counts[colour]
                        == colour_feedback_count[colour]
                    ):
                        self.completed_colours.add(colour)

                    if colour in self.forbidden_positions:
                        self.forbidden_positions[colour].add(i)
                    else:
                        self.forbidden_positions[colour] = {i}

            if colour in self.unused_colours:
                self.unused_colours.remove(colour)

        for colour, count in colour_feedback_count.items():
            self.colour_counts[colour] = max(self.colour_counts[colour], count)

        if len(self.present_colours) + len(self.eliminated_colours) == len(
            AVAILABLE_COLOURS
        ):
            self.discovery_mode = False

    # -----------------------------------------------------
    # EVALUATE GUESS - For Algo Testing
    # -----------------------------------------------------
    def test_evaluate_guess(self, secret, guess):

        feedback = [""] * 5

        secret_remaining = []
        guess_remaining = []
        remaining_indices = []

        for i, (s, g) in enumerate(zip(secret, guess)):
            if s == g:
                feedback[i] = CORRECT
            else:
                secret_remaining.append(s)
                guess_remaining.append(g)
                remaining_indices.append(i)

        secret_counter = Counter(secret_remaining)

        for idx, g in zip(remaining_indices, guess_remaining):
            if secret_counter[g] > 0:
                feedback[idx] = MISTAKE
                secret_counter[g] -= 1
            else:
                feedback[idx] = WRONG

        return "".join(feedback)

    # -----------------------------------------------------
    # ALGO TESTING - Main Loop
    # -----------------------------------------------------
    def test_algorithm(self, secret):

        loop_count = 0
        while True:
            loop_count += 1
            self.current_guess = self.generate_guess()

            current_guess_feedback = self.test_evaluate_guess(
                secret=secret, guess=self.current_guess
            )

            if loop_count > 10:
                break

            if all(f == CORRECT for f in current_guess_feedback):
                break

            self.update_knowledge(feedback=current_guess_feedback)


# >>> Algorithm Test
# my_code = [RED, RED, WHITE, GREEN, RED]
# print(f"My Code: {my_code}")
# decoder = SystemDecoder()
# decoder.test_algorithm(my_code)
