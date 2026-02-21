# SuperMastermind
SuperMastermind is a code-breaking game played by two players. Each player tries to decode the colour-code set by the other player during their turn. The player who decodes the colour-code in less moves is declared the winner.

<hr>

## Codebase
1. Dependencies
    - customtkinter==5.2.2
    - pillow==11.3.0

2. Code Specifications
    - The application entry point is the `app.py` file.

    - The complete UI lives functionality under the `ui/` directory:
        > The `main_window.py` file is the master file for the complete GUI, response and the gameplay.\n
        > The `background.py` file consists of helper functions for rendering background effects and background images.

    - The backend Game logic and the logging mechanism are placed the `util/` directory.
        > The `logging_config.py` renders the logging mechanism for the application.\n
        > The `constants.py` file holds the centralized values for all constants, texts, strings, and colour-codes used and required across the application.\n
        > The `logics.py` file holds the backend helper and logic calculating functions for gameplay.\n
        > The `system_decoder.py` file consists of the complete System Decoding Algorithm that works with the primary objective of decoding the User's code in as less moves as possible. During gameplay, the system runs a discovery phase (randomized sampling of unused colours while learning which colours are present) followed by a placement phase where it tries to place known colours in allowed positions.

---

## User Journey
### 1. Launching the Application
- UI POV: User launches the application by executing `app.py` from the terminal.
	> `python app.py`
[Image]

- Code POV:
    > Logging mechanism is initialized. App-level logging is configured by `util/logging_config.py` and uses constants from `util/constants.py`.
    > The GUI for the application is rendered. The window uses `customtkinter` for modern widgets. The background fades in using the `open_background_app()` helper in `ui/background.py`.

### 2. Home Screen
- UI POV: User sees the Home screen.
	> App title and a short subtitle.
	> Two Call-To-Actions (CTAs): `NEW GAME` and `READ INSTRUCTIONS`.
[Image]

- Code POV:
    > Rendered from `MainWindow._display_home_screen` in `ui/main_window.py`.

### 3. Instructions Screen
- UI POV: User clicks the `READ INSTRUCTIONS` button. The App opens the Instructions screen.
	> The instructions are displayed inside a styled, read-only textbox.
	> The `BACK` CTA button takes the user back to the home screen.
[Image]

- Code POV:
    > Rendered from `MainWindow._display_instructions_screen` in `ui/main_window.py`.

### 4. Choose Task (Set-Code / De-Code)
- UI POV: When starting a new game, User chooses a task on the `CHOOSE TASK` screen.
	> If the user selects `SET-CODE`, the user will set the secret code first and the system will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the system will set the code and the user will attempt to decode it.
	> If the user selects the `DE-CODE`, the system sets the secret code first and the user will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the user will set the code and the system will attempt to decode it.
[Image]

- Code POV:
    > Rendered from `MainWindow_display_choose_task_screen` in `ui/main_window.py`.
    > User's role selection is handled by `MainWindow._handle_user_taskscreen_choice` in `ui/main_window.py`.

### 5. Gameplay Load
- UI POV: After choosing a role, User sees the loading screen briefly (for about 5 seconds).
[Image]

- Code POV:
    > Rendered from `MainWindow._display_gameplay_load_screen` in `ui/main_window.py`.

### 6. Gameplay Screen Layout
- UI POV: Post the brief interval, the loading screen transitions to the gameplay screen. User sees the gameplay screen which is split across 3-panels:
    - Left panel (Screen A):
        > Shows the current role labels (USER / SYSTEM) and a prominent `START ▶` button to begin the turn flow.
[Image]

    - Center board (Screen B):
        > This is the game board - interactive area where guesses are filled and feedbacks are shown.
        > There are five slot buttons representing the code positions. The slots let the player choose colours when setting a code or entering a guess.
        > Turn-by-turn guesses and feedback are displayed on the board.
[Image]

    - Right panel (Screen C):
        > Acts as the chat / message area. System messages (taunts, prompts, warnings) are appended here.
        > The right panel also has an `EXIT ▶` button to end the game and return to home screen.
[Image]

- Code POV:
    > Rendered from `MainWindow._display_gameplay_screen` in `ui/main_window.py`.

### 7. Roles and Turn Transitions
- UI POV:
    - If the user chose `SET-CODE` initially:
	    > User is prompted to pick colours for the 5-slot code using the UI slot buttons. The code should be a list of 5 colour names.
	    > Once the user sets the code and starts, the system will try to guess and decode the code.
[Image]

    - If the user chose `DE-CODE`:
	    > The system creates a secret code, and the user attempts to decode it by making guesses on the center board.
[Image]

- Code POV:
    > The system uses `SystemDecoder` algorithm from `util/system_decoder.py` during its turn to decode in order to generate guesses and to update its internal knowledge from feedback.
    > The system uses `util/logics.create_colour_code()` and its internal logic calculating functions to improve the code-set difficulty during its turn to set code.

### 8. Guess Evaluation and Feedback
- UI POV: After each guess, the guess is evaluated and the feedback is presented per-slot, and User sees the updated UI consisting of turn counters and feedback labels.
    > Each guess is evaluated and per-position feedback is returned: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).
[Image]

- Code POV:
    > Each guess is evaluated with `util/logics.evaluate_guess()` which returns per-position feedback: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).
    > For the system solver: `SystemDecoder.update_knowledge()` collects present colours, forbidden positions, eliminated colours and fills `colour_counts`, then switches from discovery to placement mode when appropriate.

### 9. Revealing and End Game
- UI POV:
    > If the user clicks on reveal system code early (the UI shows a reveal button), the user loses the game and a message is shown in the chat area.
[Image]

    > NOTE: The "Show/View/Hide Code" is only for the user to quickly view the secret code they have set in case they forget their code. It won't reveal the code to the system and won't result in game loss for the user.
[Image]

    > When the code is cracked (all positions correct), the UI shows a success message with the number of turns and the right panel logs the win or tie messages. Whoever decodes the other's code in less moves is declared the winner.
[Image]

    > If both the user's and the system's turns to decode on another are the same, the game ends in a tie.
[Image]

---

Final Note:
Just built this game as I wanted to re-visit and re-feel the coding experience after a long time.
Feel free to use, play, enjoy, and modify the application and the game. I'm always open for feedback, suggestions and improvements.
Peace
