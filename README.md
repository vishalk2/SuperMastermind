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
        > The `main_window.py` file is the master file for the complete GUI, response and the gameplay.<br>
        > The `background.py` file consists of helper functions for rendering background effects and background images.

    - The backend Game logic and the logging mechanism are placed the `util/` directory.
        > The `logging_config.py` renders the logging mechanism for the application.<br>
        > The `constants.py` file holds the centralized values for all constants, texts, strings, and colour-codes used and required across the application.<br>
        > The `logics.py` file holds the backend helper and logic calculating functions for gameplay.<br>
        > The `system_decoder.py` file consists of the complete System Decoding Algorithm that works with the primary objective of decoding the User's code in as less moves as possible. During gameplay, the system runs a discovery phase (randomized sampling of unused colours while learning which colours are present) followed by a placement phase where it tries to place known colours in allowed positions.<br>

<hr>

## User Journey
### 1. Launching the Application
- UI POV: User launches the application by executing `app.py` from the terminal.
	> `python app.py`<br>
<img width="1367" height="622" alt="image" src="https://github.com/user-attachments/assets/20c7dc62-3a5a-456f-9b94-bc61c8c0b049" />
<br>

- Code POV:
    > Logging mechanism is initialized. App-level logging is configured by `util/logging_config.py` and uses constants from `util/constants.py`.<br>
    > The GUI for the application is rendered. The window uses `customtkinter` for modern widgets. The background fades in using the `open_background_app()` helper in `ui/background.py`.<br>

### 2. Home Screen
- UI POV: User sees the Home screen.
	> App title and a short subtitle.<br>
	> Two Call-To-Actions (CTAs): `NEW GAME` and `READ INSTRUCTIONS`.<br>
<img width="1365" height="720" alt="image" src="https://github.com/user-attachments/assets/7fcaac1f-9a56-48fc-a809-684cfa55c2f7" />
<br>

- Code POV:
    > Rendered from `MainWindow._display_home_screen` in `ui/main_window.py`.<br>

### 3. Instructions Screen
- UI POV: User clicks the `READ INSTRUCTIONS` button. The App opens the Instructions screen.
	> The instructions are displayed inside a styled, read-only textbox.<br>
	> The `BACK` CTA button takes the user back to the home screen.<br>
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/52019114-b1b1-4d18-8f3e-f0aac8a28c25" />
<br>

- Code POV:
    > Rendered from `MainWindow._display_instructions_screen` in `ui/main_window.py`.<br>

### 4. Choose Task (Set-Code / De-Code)
- UI POV: When starting a new game, User chooses a task on the `CHOOSE TASK` screen.
	> If the user selects `SET-CODE`, the user will set the secret code first and the system will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the system will set the code and the user will attempt to decode it.<br>
	> If the user selects the `DE-CODE`, the system sets the secret code first and the user will attempt to decode it. Once the system completes decoding the user's code, the roles are reversed and the 2nd part of the game is rendered: the user will set the code and the system will attempt to decode it.<br>
<img width="1365" height="720" alt="image" src="https://github.com/user-attachments/assets/f2ded457-6257-46db-a1d7-3d4104da9320" />
<br>

- Code POV:
    > Rendered from `MainWindow_display_choose_task_screen` in `ui/main_window.py`.<br>
    > User's role selection is handled by `MainWindow._handle_user_taskscreen_choice` in `ui/main_window.py`.<br>

### 5. Gameplay Load
- UI POV: After choosing a role, User sees the loading screen briefly (for about 5 seconds) - with a "SET-CODE"/"DE-CODE" role mentioned based on their initial selection.
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/b7a3d317-9f45-408f-9569-c0df11191b77" />
<br>

- Code POV:
    > Rendered from `MainWindow._display_gameplay_load_screen` in `ui/main_window.py`.<br>

### 6. Gameplay Screen Layout
- UI POV: Post the brief interval, the loading screen transitions to the gameplay screen. User sees the gameplay screen which is split across 3-panels:
    - Left panel (Screen A):
        > Shows the current role labels (USER / SYSTEM) and a prominent `START ▶` button to begin the turn flow.<br>
<img width="1366" height="722" alt="image" src="https://github.com/user-attachments/assets/3c49483a-3306-4ef6-9293-e5b614652f2b" />
<br>

    - Center board (Screen B):
        > This is the game board - interactive area where guesses are filled and feedbacks are shown.<br>
        > There are five slot buttons representing the code positions. The slots let the player choose colours when setting a code or entering a guess.<br>
        > Turn-by-turn guesses and feedback are displayed on the board.<br>
<img width="1365" height="719" alt="image" src="https://github.com/user-attachments/assets/bc24d2ab-4ed3-41ea-b0cd-29cc954c25a8" />
<br>

    - Right panel (Screen C):
        > Acts as the chat / message area. System messages (taunts, prompts, warnings) are appended here.<br>
        > The right panel also has an `EXIT ▶` button to end the game and return to home screen.<br>
<img width="1365" height="721" alt="image" src="https://github.com/user-attachments/assets/d2315a25-e1b5-4593-8f35-ec66a35fd0a8" />
<br>

- Code POV:
    > Rendered from `MainWindow._display_gameplay_screen` in `ui/main_window.py`.<br>

### 7. Roles and Turn Transitions
- UI POV:
    - If the user chose `SET-CODE` initially:
	    > User is prompted to pick colours for the 5-slot code using the UI slot buttons. The code should be a list of 5 colour names.<br>
	    > Once the user sets the code and starts, the system will try to guess and decode the code.<br>
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/2e76d5cf-a0e1-4a4a-9f43-c1c20a166b08" />
<br>

    - If the user chose `DE-CODE`:
	    > The system creates a secret code, and the user attempts to decode it by making guesses on the center board.<br>
<img width="1365" height="715" alt="image" src="https://github.com/user-attachments/assets/ea029b0d-9956-4661-90ba-c0d9c9896c33" />
<br>

- Code POV:
    > The system uses `SystemDecoder` algorithm from `util/system_decoder.py` during its turn to decode in order to generate guesses and to update its internal knowledge from feedback.<br>
    > The system uses `util/logics.create_colour_code()` and its internal logic calculating functions to improve the code-set difficulty during its turn to set code.<br>

### 8. Guess Evaluation and Feedback
- UI POV: After each guess, the guess is evaluated and the feedback is presented per-slot, and User sees the updated UI consisting of turn counters and feedback labels.
    > Each guess is evaluated and per-position feedback is returned: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).<br>
<img width="1365" height="718" alt="image" src="https://github.com/user-attachments/assets/b040ae57-212a-4e01-9737-846069407a1a" />
<br>

- Code POV:
    > Each guess is evaluated with `util/logics.evaluate_guess()` which returns per-position feedback: correct-placement (✅), present-wrong-place (⚠️), or not-present (❌).<br>
    > For the system solver: `SystemDecoder.update_knowledge()` collects present colours, forbidden positions, eliminated colours and fills `colour_counts`, then switches from discovery to placement mode when appropriate.<br>

### 9. Revealing and End Game
- UI POV:
    > If the user clicks on reveal system code early (the UI shows a reveal button), the user loses the game and a message is shown in the chat area.<br>
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/9a5f92a7-fa55-4deb-943b-77d71c91759c" />
<br>

    > NOTE: The "View/Hide Code" is only for the user to quickly view and hide the secret code they have set in case they forget their code. It won't reveal the code to the system and won't result in game loss for the user.<br>
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/03031fd6-f8b4-4ce5-9b00-6ee05bd3a0a6" />
<br>

    > When the code is cracked (all positions correct), the UI shows a success message with the number of turns and the right panel logs the win or tie messages. Whoever decodes the other's code in less moves is declared the winner.<br>
<img width="1365" height="718" alt="image" src="https://github.com/user-attachments/assets/f31439e3-f118-4845-b15c-673136c72fbd" />


    > If both the user's and the system's turns to decode on another are the same, the game ends in a tie.<br>

<hr>

Final Note:
Just built this game as I wanted to re-visit and re-feel the coding experience after a long time.
Feel free to use, play, enjoy, and modify the application and the game. I'm always open for feedback, suggestions and improvements.
Peace :v:
