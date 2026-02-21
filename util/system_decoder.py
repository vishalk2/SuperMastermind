import random
from collections import Counter

COLOUR_OPTIONS = [
    "RED",
    "ORANGE",
    "YELLOW",
    "GREEN",
    "BLUE",
    "PURPLE",
    "BROWN",
    "BLACK",
    "WHITE",
]

CORRECT = "Y"
WRONG = "N"
MISTAKE = "M"


# >>>
def evaluate_guess(secret, guess):

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


class SystemDecoder:

    def __init__(self):

        self.turn = 0
        self.current_guess = []

        self.present_colours = set()
        self.eliminated_colours = set()
        self.completed_colours = set()

        self.correct_positions = dict()  # index -> colour
        self.forbidden_positions = dict()  # colour -> {indices}

        self.colour_counts = Counter()
        self.unused_colours = COLOUR_OPTIONS.copy()
        self.discovery_mode = True
        self.discovery_guess_count = 0
        self.placement_guess_count = 0
        print("Completed initializing state variables.")

    # -----------------------------------------------------
    # GENERATE NEXT GUESS
    # -----------------------------------------------------
    def generate_guess(self):

        self.turn = self.turn + 1

        if self.turn == 1:
            self.current_guess = random.sample(COLOUR_OPTIONS, 5)
            return self.current_guess

        if self.discovery_mode == True and len(self.present_colours) < 5:
            self.current_guess = self.discovery_guess()
            return self.current_guess

        self.current_guess = self.placement_guess()
        return self.current_guess

    # -----------------------------------------------------
    # DISCOVERY PHASE
    # -----------------------------------------------------
    def discovery_guess(self):
        print("---")
        print(f"Turn: {self.turn} | Discover Guess")

        self.discovery_guess_count += 1

        new_guess = [None] * 5
        print(f"New Guess: {new_guess}")

        for idx, colour in self.correct_positions.items():
            new_guess[idx] = colour
        print(f"Guess after filling correct positions: {new_guess}")

        remaining_slots = {i for i, c in enumerate(new_guess) if c is None}
        print(f"Remaining Slots: {remaining_slots}")

        for colour, indices in self.forbidden_positions.items():

            if colour in self.completed_colours:
                continue

            if colour in self.correct_positions.values():
                continue

            forbidden_slots = set(map(int, indices))
            available_slots = list(remaining_slots - forbidden_slots)

            print(f"Colour: {colour} | Forbidden Positions: {forbidden_slots}")
            print(f"Available Slots: {available_slots}")

            if not available_slots:
                continue

            new_idx = random.choice(available_slots)
            new_guess[new_idx] = colour
            remaining_slots.remove(new_idx)
            print(f"Chosen Index: {new_idx}")
            print(f"Remaining Slots: {remaining_slots}")
            print(f"New Guess: {new_guess}")

        for idx in list(remaining_slots):

            print(f"idx: {idx} | Unused Colours: {self.unused_colours}")
            present_colours = list(self.present_colours)

            if self.unused_colours:
                colour = random.choice(list(self.unused_colours))
                new_guess[idx] = colour
                self.unused_colours.remove(colour)
                print(f"Added colours from unused_colours: {colour}")

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
                    print(f"Added colours from present_colours: {new_guess[idx]}")
                    break

            else:
                new_guess[idx] = random.choice(new_guess[:4])
                print(
                    f"Added colours from current colours in new_guess: {new_guess[idx]}"
                )

        print(f"Final guess in discovery mode: {new_guess}")
        print("---")

        return new_guess

    # -----------------------------------------------------
    # PLACEMENT PHASE
    # -----------------------------------------------------
    def placement_guess(self):
        print("---")
        print(f"Turn: {self.turn} | Placement Guess")
        self.placement_guess_count += 1

        new_guess = [None] * 5
        print(f"New Guess: {new_guess}")

        print(f"Present Colours: {self.present_colours}")
        print(f"Correct positions: {self.correct_positions}")

        if len(self.present_colours) == 1:
            new_guess = [list(self.present_colours)[0]] * 5
            return new_guess

        for idx, colour in self.correct_positions.items():
            new_guess[idx] = colour
        print(f"Guess after filling correct positions: {new_guess}")

        remaining_slots = {i for i in range(5) if new_guess[i] is None}
        print(f"Remaining Slots: {remaining_slots}")

        if len(self.present_colours) == 2:

            for colour, indices in self.forbidden_positions.items():

                if (
                    colour in self.completed_colours
                ):
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots

                print(f"Colour: {colour}")
                print(f"Forbidden Slots: {forbidden_slots}")
                print(f"Allowed Slots: {allowed_slots}")

                if not allowed_slots:
                    continue

                for idx in allowed_slots:
                    new_guess[idx] = colour

                remaining_slots = remaining_slots - allowed_slots
                print(f"Remaining Slots: {remaining_slots}")

            if remaining_slots:

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in self.present_colours
                }
                print(f"Forbidden Counts: {forbidden_counts}")

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                print(f"Preferred Colour for remaining slots: {preferred_colour}")

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

            print(f"Final New Guess: {new_guess}")

        if len(self.present_colours) == 3:

            for colour, indices in self.forbidden_positions.items():

                if (
                    colour in self.completed_colours
                ):
                    continue

                correct_colour_counts = Counter(self.correct_positions.values())
                if (
                    colour in self.correct_positions.values()
                    and correct_colour_counts[colour] == self.colour_counts[colour]
                ):
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots

                print(f"Colour: {colour}")
                print(f"Forbidden Slots: {forbidden_slots}")
                print(f"Allowed Slots: {allowed_slots}")

                if not allowed_slots:
                    continue

                # for idx in allowed_slots:
                #     new_guess[idx] = colour
                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)
                print(f"Chosen Index: {new_idx}")
                print(f"Remaining Slots: {remaining_slots}")
                print(f"New Guess: {new_guess}")

                # remaining_slots -= allowed_slots
                print(f"Remaining Slots: {remaining_slots}")

            if remaining_slots:

                for idx in remaining_slots:
                    print(f"idx: {idx} in remaining slots")

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
                    print(f"Candidate Colours for remaining slots: {candidate_colours}")

                    forbidden_counts = {
                        colour: len(self.forbidden_positions.get(colour, []))
                        for colour in candidate_colours
                    }
                    print(f"Forbidden Counts: {forbidden_counts}")

                    preferred_colour = min(forbidden_counts, key=forbidden_counts.get)
                    print(f"Preferred Colour for remaining slots: {preferred_colour}")

                    new_guess[idx] = preferred_colour

            print(f"Final New Guess: {new_guess}")

        if len(self.present_colours) == 4:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours and self.placement_guess_count > 1:
                    continue

                if colour in self.correct_positions.values():
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots

                print(f"Colour: {colour}")
                print(f"Forbidden Slots: {forbidden_slots}")
                print(f"Allowed Slots: {allowed_slots}")

                if not allowed_slots:
                    continue

                # for idx in allowed_slots:
                #     new_guess[idx] = colour
                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)
                print(f"Chosen Index: {new_idx}")
                print(f"Remaining Slots: {remaining_slots}")
                print(f"New Guess: {new_guess}")

                # remaining_slots -= allowed_slots
                print(f"Remaining Slots: {remaining_slots}")

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
                print(f"Candidate Colours for remaining slots: {candidate_colours}")

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in candidate_colours
                }
                print(f"Forbidden Counts: {forbidden_counts}")

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                double_count_colour = None
                for colour in candidate_colours:
                    if self.colour_counts.get(colour, 0) > 1:
                        double_count_colour = colour
                        break
                if double_count_colour != None:
                    preferred_colour = double_count_colour

                print(f"Preferred Colour for remaining slots: {preferred_colour}")

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

            print(f"Final New Guess: {new_guess}")

        if len(self.present_colours) == 5:

            for colour, indices in self.forbidden_positions.items():

                if colour in self.completed_colours:
                    continue

                if colour in self.correct_positions.values():
                    continue

                forbidden_slots = set(map(int, indices))
                allowed_slots = remaining_slots - forbidden_slots

                print(f"Colour: {colour}")
                print(f"Forbidden Slots: {forbidden_slots}")
                print(f"Allowed Slots: {allowed_slots}")

                if not allowed_slots:
                    continue

                # for idx in allowed_slots:
                #     new_guess[idx] = colour
                new_idx = random.choice(list(allowed_slots))
                new_guess[new_idx] = colour
                allowed_slots.remove(new_idx)
                remaining_slots.remove(new_idx)
                print(f"Chosen Index: {new_idx}")
                print(f"Remaining Slots: {remaining_slots}")
                print(f"New Guess: {new_guess}")

                # remaining_slots -= allowed_slots
                print(f"Remaining Slots: {remaining_slots}")

            if remaining_slots:

                candidate_colours = [
                    c for c in self.present_colours if c not in self.completed_colours
                ]
                if not candidate_colours:
                    candidate_colours = list(self.present_colours)
                print(f"Candidate Colours for remaining slots: {candidate_colours}")

                forbidden_counts = {
                    colour: len(self.forbidden_positions.get(colour, []))
                    for colour in candidate_colours
                }
                print(f"Forbidden Counts: {forbidden_counts}")

                preferred_colour = min(forbidden_counts, key=forbidden_counts.get)

                print(f"Preferred Colour for remaining slots: {preferred_colour}")

                for idx in remaining_slots:
                    new_guess[idx] = preferred_colour

            print(f"Final New Guess: {new_guess}")

        return new_guess

    # -----------------------------------------------------
    # UPDATE KNOWLEDGE
    # -----------------------------------------------------
    def update_knowledge(self, feedback):

        colour_feedback_count = Counter()

        # Update knowledge for correctly placed colours first
        for i, (colour, fb) in enumerate(zip(self.current_guess, feedback)):
            if fb == CORRECT:
                self.present_colours.add(colour)
                self.correct_positions[i] = colour
                colour_feedback_count[colour] += 1

        # Then update knowledge for mistakes
        for i, (colour, fb) in enumerate(zip(self.current_guess, feedback)):
            if fb == MISTAKE:
                self.present_colours.add(colour)

                if colour in self.forbidden_positions:
                    self.forbidden_positions[colour].add(i)
                else:
                    self.forbidden_positions[colour] = {i}

                colour_feedback_count[colour] += 1

        # Finally, update knowledge for wrong positions
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

        print(f"Present Colours: {self.present_colours}")
        print(f"Correct Positions: {self.correct_positions}")
        print(f"Forbidden Positions: {self.forbidden_positions}")
        print(f"Eliminated Colours: {self.eliminated_colours}")
        print(f"Unused Colours: {self.unused_colours}")
        print(f"Completed Colours: {self.completed_colours}")

        for colour, count in colour_feedback_count.items():
            self.colour_counts[colour] = max(self.colour_counts[colour], count)
        print(f"Colour Counts: {self.colour_counts}")

        if len(self.present_colours) + len(self.eliminated_colours) == len(
            COLOUR_OPTIONS
        ):
            self.discovery_mode = False
            print("Discovery mode is set to false.")

        print("---")

    # -----------------------------------------------------
    # MAIN LOOP (FOR TESTING)
    # -----------------------------------------------------
    def solve(self, secret):

        loop_count = 0
        while True:
            loop_count += 1
            self.current_guess = self.generate_guess()

            current_guess_feedback = evaluate_guess(
                secret=secret, guess=self.current_guess
            )

            print(
                f"Turn {self.turn}: "
                + f"{self.current_guess}"
                + f" -> {current_guess_feedback}"
            )

            if loop_count > 10:
                break

            if all(f == CORRECT for f in current_guess_feedback):
                print(f"\nSolved in {self.turn} turns!")
                break

            self.update_knowledge(feedback=current_guess_feedback)


# >>> Test
my_code = ["WHITE", "BLUE", "YELLOW", "BLUE", "BLACK"]
print(f"My Code: {my_code}")
decoder = SystemDecoder()
decoder.solve(my_code)
