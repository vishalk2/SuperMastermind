# SuperMastermind
SuperMastermind is a code-breaking game played by two players. Each player tries to decode the colour-code set by the other player during their turn. The player who decodes the colour-code in less moves is declared the winner.

<hr>

## Gameplay >>>

<br>
<video src="https://github.com/user-attachments/assets/201b7e80-52e8-4865-a539-57cf986a9883"></video>
<br>

<hr>

## Codebase
1. Dependencies
    - customtkinter==5.2.2
    - pillow==11.3.0

2. Code Specifications
    - The application entry point is the `app.py` file.

    - The complete UI lives functionality under the `ui/` directory:
        > - The `main_window.py` file is the master file for the complete GUI, response and the gameplay.<br>
        > - The `background.py` file consists of helper functions for rendering background effects and background images.

    - The backend Game logic and the logging mechanism are placed the `util/` directory.
        > - The `logging_config.py` renders the logging mechanism for the application.<br>
        > - The `constants.py` file holds the centralized values for all constants, texts, strings, and colour-codes used and required across the application.<br>
        > - The `logics.py` file holds the backend helper and logic calculating functions for gameplay.<br>
        > - The `system_decoder.py` file consists of the complete System Decoding Algorithm that works with the primary objective of decoding the User's code in as less moves as possible. During gameplay, the system runs a discovery phase (randomized sampling of unused colours while learning which colours are present) followed by a placement phase where it tries to place known colours in allowed positions.<br>

<hr>

## User Journey
### 1. Launching the Application
- UI POV: User launches the application by executing `app.py` from the terminal.
	> `python app.py`<br>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/20c7dc62-3a5a-456f-9b94-bc61c8c0b049" />
<br>

- Code POV:
    > - Logging mechanism is initialized. App-level logging is configured by `util/logging_config.py` and uses constants from `util/constants.py`.<br>
    > - The GUI for the application is rendered. The window uses `customtkinter` for modern widgets. The background fades in using the `open_background_app()` helper in `ui/background.py`.<br>

<br>

### 2. Home Screen
- UI POV: User sees the Home screen.
	> - App title and a short subtitle.<br>
	> - Two Call-To-Actions (CTAs): `NEW GAME` and `READ INSTRUCTIONS`.<br>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/7fcaac1f-9a56-48fc-a809-684cfa55c2f7" />
<br>

- Code POV:
    > - Rendered from `MainWindow._display_home_screen` in `ui/main_window.py`.<br>

<br>

### 3. Instructions Screen
- UI POV: User clicks the `READ INSTRUCTIONS` button. The App opens the Instructions screen.
	> - The instructions are displayed inside a styled, read-only textbox.<br>
	> - The `BACK` CTA button takes the user back to the home screen.<br>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/52019114-b1b1-4d18-8f3e-f0aac8a28c25" />
<br>

- Code POV:
    > - Rendered from `MainWindow._display_instructions_screen` in `ui/main_window.py`.<br>

<br>

### 4. Choose Task (Set-Code / De-Code)
- UI POV: When starting a new game, User chooses a task on the `CHOOSE TASK` screen.
	> - If the user selects `SET-CODE`, the user will set the secret code first and the system will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the system will set the code and the user will attempt to decode it.<br>
	> - If the user selects the `DE-CODE`, the system sets the secret code first and the user will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the user will set the code and the system will attempt to decode it.<br>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/f2ded457-6257-46db-a1d7-3d4104da9320" />
<br>

- Code POV:
    > - Rendered from `MainWindow_display_choose_task_screen` in `ui/main_window.py`.<br>
    > - User's role selection is handled by `MainWindow._handle_user_taskscreen_choice` in `ui/main_window.py`.<br>

<br>

### 5. Gameplay Load
- UI POV: After choosing a role, User sees the loading screen briefly (for about 5 seconds) - with a "SET-CODE"/"DE-CODE" role mentioned based on their initial selection.
<img width="800" alt="image" src="https://github.com/user-attachments/assets/b7a3d317-9f45-408f-9569-c0df11191b77" />
<br>

- Code POV:
    > - Rendered from `MainWindow._display_gameplay_load_screen` in `ui/main_window.py`.<br>

<br>

### 6. Gameplay Screen Layout

Post the brief interval, the loading screen transitions to the gameplay screen. The gameplay screen is split across three panels:

#### Left panel (Screen A)

- Shows the current role labels (USER / SYSTEM) and a prominent `START ▶` button to begin the turn flow.

<img width="800" alt="Left panel" src="https://github.com/user-attachments/assets/3c49483a-3306-4ef6-9293-e5b614652f2b" />

#### Center board (Screen B)

- This is the game board — the interactive area where guesses are entered and feedback is shown.
- There are five slot buttons representing the code positions. The slots let the player choose colours when setting a code or entering a guess.
- Turn-by-turn guesses and feedback are displayed on the board.

<img width="800" alt="Center board" src="https://github.com/user-attachments/assets/bc24d2ab-4ed3-41ea-b0cd-29cc954c25a8" />

#### Right panel (Screen C)

- Acts as the chat / message area. System messages (taunts, prompts, warnings) are appended here.
- The right panel also has an `EXIT ▶` button to end the game and return to the home screen.

<img width="800" alt="Right panel" src="https://github.com/user-attachments/assets/d2315a25-e1b5-4593-8f35-ec66a35fd0a8" />

**Code POV:**

> - Rendered from `MainWindow._display_gameplay_screen` in `ui/main_window.py`.


### 7. Roles and Turn Transitions

The roles determine who sets the code and who decodes it. There are two primary flows:

#### If the user chose `SET-CODE`

- The user is prompted to pick colours for the 5-slot code using the UI slot buttons. The code should be a list of 5 colour names.
- Once the user sets the code and starts, the system will attempt to guess and decode the code using its solver.

<img width="800" alt="User set code" src="https://github.com/user-attachments/assets/2e76d5cf-a0e1-4a4a-9f43-c1c20a166b08" />

#### If the user chose `DE-CODE`

- The system creates a secret code (via `create_colour_code()`), and the user attempts to decode it by making guesses on the center board.

<img width="800" alt="System set code" src="https://github.com/user-attachments/assets/ea029b0d-9956-4661-90ba-c0d9c9896c33" />

**Code POV:**

- The system uses the `SystemDecoder` algorithm in `util/system_decoder.py` to generate guesses and update its knowledge from feedback.
- The system uses `util/logics.create_colour_code()` when it needs to set a code for the user to decode.


### 8. Guess Evaluation and Feedback
- UI POV: After each guess, the guess is evaluated and the feedback is presented per-slot, and User sees the updated UI consisting of turn counters and feedback labels.
    > - Each guess is evaluated and per-position feedback is returned: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).<br>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/b040ae57-212a-4e01-9737-846069407a1a" />
<br>

- Code POV:
    > - Each guess is evaluated with `util/logics.evaluate_guess()` which returns per-position feedback: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).<br>
    > - For the system solver: `SystemDecoder.update_knowledge()` collects present colours, forbidden positions, eliminated colours and fills `colour_counts`, then switches from discovery to placement mode when appropriate.<br>

<br>

### 9. Revealing and End Game

The game can end in a few ways depending on player actions and successful decoding:

#### Early reveal (user)

- If the user reveals the system's code early using the reveal control, the user forfeits and the system logs the win in the chat area.

<img width="800" alt="Reveal code" src="https://github.com/user-attachments/assets/9a5f92a7-fa55-4deb-943b-77d71c91759c" />

#### View/Hide Code (user convenience)

- The `View/Hide Code` control only toggles the user's own code visibility (so they don't forget what they set). It does not expose the code to the system and does not cause a loss.

<img width="800" alt="View hide code" src="https://github.com/user-attachments/assets/03031fd6-f8b4-4ce5-9b00-6ee05bd3a0a6" />

#### Successful decode

- When a code is cracked (all five positions correct), the UI displays a success message with the number of turns taken. The right panel logs the win or tie messages and the game ends.

<img width="800" alt="End game success" src="https://github.com/user-attachments/assets/f31439e3-f118-4845-b15c-673136c72fbd" />

- If both the user and system finish decoding in the same number of turns, the game ends in a tie.

---

Final Note:
<br>
Just built this game as I wanted to re-visit and re-feel the coding experience after a long time.
<br>
Feel free to use, play, enjoy, and modify the application and the game. I'm always open for feedback, suggestions and improvements.
<br>
Peace :v:
