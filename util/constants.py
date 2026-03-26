# Application Related
APP_NAME = "SuperMastermind"

# Status
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"

# Logging
LOG_DIRECTORY = "../SuperMastermind"
LOG_FILENAME = "SuperMastermind.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
LOG_DATETIME = "%H:%M:%S"

# Emojis
CORRECT_PLACEMENT_EMOJI = "✅"
WRONG_PLACEMENT_EMOJI = "⚠️"
NOT_PRESENT_EMOJI = "❌"

CORRECT = "Y"
WRONG = "N"
MISTAKE = "M"

# HTML Colour Codes
RED = "#FF0000"
ORANGE = "#FF6F00"
YELLOW = "#F6FF00"
GREEN = "#04FF00"
BLUE = "#0048FF"
PURPLE = "#9900FF"
BROWN = "#6B1700"
BLACK = "#000000"
WHITE = "#FFFFFF"
GREY = "#C0C0C0"
PINK = "#FF00FF"
CYAN = "#00FFFF"
TEAL = "#008080"
INDIGO = "#480082"
KHAKI = "#808000"
AVAILABLE_COLOURS = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    PURPLE,
    BROWN,
    BLACK,
    WHITE,
    GREY,
    PINK,
    CYAN,
    TEAL,
    INDIGO,
    KHAKI
]
COLOUR_MAP = {
    "RED": RED,
    "ORANGE": ORANGE,
    "YELLOW": YELLOW,
    "GREEN": GREEN,
    "BLUE": BLUE,
    "PURPLE": PURPLE,
    "BROWN": BROWN,
    "BLACK": BLACK,
    "WHITE": WHITE,
    "GREY": GREY,
    "PINK": PINK,
    "CYAN": CYAN,
    "TEAL": TEAL,
    "INDIGO": INDIGO,
    "KHAKI": KHAKI,
}
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
    "GREY",
    "PINK",
    "CYAN",
    "TEAL",
    "INDIGO",
    "KHAKI"
]

# Game Constants
CODE_LENGTH = 5
USER = "YOU"
SYSTEM = "SYSTEM"
SET_CODE = "SET-CODE"
DE_CODE = "DE-CODE"
HEADER_SLOT = "HEADER"
TEXT = "TEXT"
LABEL = "LABEL"

# UI - Screens
HOME_SCREEN = "HOME"
INSTRUCTIONS_SCREEN = "INSTRUCTIONS"
CHOOSE_TASK_SCREEN = "CHOOSE TASK"

# UI - Instructions
GAME_INSTRUCTIONS = (
    "1. SuperMastermind is a code-breaking game where two players take turns setting and "
    "guessing a        secret code.\n\n"
    "2. The objective of the game is to guess the secret code set by the opponent.\n\n"
    "3. In this game, one of the players is the SYSTEM (the computer) and the other player "
    "is YOU (the     user).\n\n"
    "4. The game consists of two rounds. In the first round, one player sets the code and "
    "the other player    tries to decode it. In the second round, the roles are reversed.\n\n"
    "5. The code is made up of a sequence of colors, and the player trying to decode the "
    "code will             receive feedback on their guesses.\n\n"
    "6. There are a total of 15 colours available, and the secret code consists of 5 slots to fill.\n\n"
    "7. The feedback for each guess is given in the form of emojis:\n"
    "        > '✅' for correct color in correct position\n"
    "        > '⚠️' for correct color in wrong position\n"
    "        > '❌' for incorrect color.\n\n"
    "8. The player who successfully decodes the opponent's code in the fewest number of turns wins "
    "the     game.\n\n"
    "So, are you ready to challenge the SYSTEM and become the ultimate SuperMastermind?\n"
    "Let's get started!"
)

# UI - Screen A (Left Panel) Labels
SCREEN_A_USER_LABEL = "👤"
SCREEN_A_SYSTEM_LABEL = "     🖥️"

# UI - Board - Slot Buttons
BTN1 = "btn1"
BTN2 = "btn2"
BTN3 = "btn3"
BTN4 = "btn4"
BTN5 = "btn5"
ADD_BTN = "add_btn"
ADD_BTN_HEADER_TEXTS = {USER: "REVEAL CODE ▶", SYSTEM: "ENCRYPT CODE ▶"}

# System Chats
SYSTEM_WELCOME_TEXT = """So Mr. Player, welcome to SuperMastermind.
Since neither of us wants to waste our time, let's get started.
Click on the 'START' button to start."""

SYSTEM_START_GAME_TEXT_FOR_USER_DECODE = """Since you have chosen to decode first,
I will set the code first, and you can start decoding once I'm ready."""

SYSTEM_START_GAME_TEXT_FOR_SYSTEM_DECODE = """Since you have chosen to set code first,
you will set the code first, and I will start decoding once you're ready."""

SYSTEM_EXIT_WARNING = """At any point in time during the game,
if you want to be a LOSER and want to exit the game, click on the EXIT button below."""

SYSTEM_SET_CODE_TEXT = """I have set the secret code. Do you have what it takes to crack it?
Then go ahead and show me what SuperMastermind you are! Noob ;)"""

SYSTEM_REVEAL_CODE_WARNING_TEXT = """Oh by the way, if you click
on the 'REVEAL CODE ▶' button at any point of time in the game before you crack my code, you LOSE.
Want to be a Noob? Go ahead and click on 'REVEAL CODE ▶' ;)"""

SYSTEM_REPLY_TO_USER_REVEAL_CODE_TEXT = """So you've done it, heh.
I knew you were a Noob. Couldn't crack my Code? Accept it or not, I WIN!
This is GAME OVER! Now click on EXIT & GO HOME Noob.
Come back when you are ready! Hehe."""

SYSTEM_PROMPT_USER_TO_SET_CODE_TEXT = """Yo Noob! You can SET CODE now.
Let's see how many turns I take to crack it."""

SYSTEM_REPLY_TO_USER_CRACKING_CODE = """Well, well noob. You did it.
Who knew you would be able to crack my code!"""

SYSTEM_NEXT_PART_TEXT = """Time to move on to next step.
We swap our turns now. Click on the 'NEXT' button to begin.
Then, click on SET/START as you see fit."""

SYSTEM_WINNING_TEXT = """Yo Noob! Told you, you had no chance against me.
I win. I GODDAMN win. Now go home and come back when you are ready!"""

SYSTEM_TIE_TEXT = """Ah, guess we are even. It's a tie.
Want to play again? What say?"""

SYSTEM_EXIT_TEXT = """In any case, it's GAME OVER.
So if you want to go back home, click on the EXIT button below.
Until next time!"""

# User Chats
USER_START_TEXT = """Sure bro. Let's get started.
I ain't quitting without winning. You better don't whine after I win."""

USER_SET_CODE_TEXT_REPLY = """Who you calling a Noob, you Noobie?
I thought I already told I ain't quitting without winning. Don't whine from now itself. Lol."""

USER_PROMPT_SYSTEM_TO_DECODE = """You ain't cracking my code, Noobie.
Not now. Now in an eternity! Keep whining."""

USER_REVEAL_CODE_REPLY = """I may have lost this game. But I'll be back.
Watch out for me, you noobie!"""

USER_REPLY_TO_SYSTEM_CRACKING_CODE = """Well Noobie! Good for you.
You finally were able to crack it. Not bad, huh!"""

USER_WINNING_TEXT = """Who's the noob now, Noobie!?
Told you I'd win. Now keep whining.
I WIN. I GODDAMN WIN!"""

USER_TIE_TEXT = """Hmm. We are even indeed given it's a tie.
Sure then. Let's go again!"""
