import customtkinter as ctk
import logging

from util.logics import (
    evaluate_guess,
    create_colour_code,
    convert_feedback_emojis_to_string,
)
from util.system_decoder import SystemDecoder
from util.constants import *
from ui.background import load_bg_image_for_canvas


logger = logging.getLogger(APP_NAME)


class MainWindow(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        logger.info("UI: Main Window instantiated.")

        # Initializing App-State Variables
        self.initial_user_role = None
        self.current_user_role = None
        self.current_system_role = None

        self.user_code = []
        self.user_current_guess = None
        self.system_code = []
        self.system_current_guess = None
        self.is_systems_code_revealed = False
        self.system_decoder = SystemDecoder()

        self.current_turn = 0
        self.user_total_turns = 0
        self.system_total_turns = 0

        self.turn_labels = dict()
        self.system_slots = dict()
        self.user_slots = dict()
        self.feedback_labels = dict()

        self.active_color_menu = None

        logger.info("UI: Initialized App-state Variables.")

        # Initializing UI Display
        self.master = master
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        logger.info("UI: Initialized UI Display.")

        self._create_game_layout()

    # ==================================================
    # UI - Screen Display
    # ==================================================
    # >>>
    def _create_game_layout(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=BLACK)
        self.main_panel.pack(fill="both", expand=True)
        logger.info("UI Display: Created Game Layout - Main Panel.")
        self._go_to_home_screen()

    # <<<

    # >>>
    def _display_home_screen(self):
        logger.info("UI Display: Rendering home screen display...")

        self.bg_canvas = ctk.CTkCanvas(self.main_panel, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.main_panel.update_idletasks()
        self.home_bg_photo = load_bg_image_for_canvas(
            screen=HOME_SCREEN,
            assets_path="assets/home_bg.jpg",
            size=(self.main_panel.winfo_width(), self.main_panel.winfo_height()),
            opacity=0.35,
        )
        self.bg_canvas.create_image(0, 0, anchor="nw", image=self.home_bg_photo)

        content = ctk.CTkFrame(
            self.bg_canvas,
            width=500,
            height=300,
            bg_color=BLACK,
            fg_color=BLACK,
        )
        content.place(relx=0.5, rely=0.5, anchor="center")
        content.pack_propagate(False)

        ctk.CTkLabel(
            content,
            text=APP_NAME,
            font=ctk.CTkFont(family="Times New Roman", size=42, weight="bold"),
            text_color=ORANGE,
        ).pack(pady=10)

        ctk.CTkLabel(
            content,
            text="Crack the code. Outsmart the system.",
            font=ctk.CTkFont(family="Times New Roman", size=20),
            text_color=YELLOW,
        ).pack(pady=5)

        ctk.CTkButton(
            content,
            text="NEW GAME",
            width=240,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._go_to_choose_task_screen,
        ).pack(pady=20)

        ctk.CTkButton(
            content,
            text="READ INSTRUCTIONS",
            width=240,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._go_to_instructions_screen,
        ).pack(pady=10)
        logger.info("UI Display: Loaded home screen content area.")

        logger.info("UI Display: Completed rendering home screen display.")
        logger.info("UI Display: Displaying home screen.")

    # <<<

    # >>>
    def _display_instructions_screen(self):
        logger.info("UI Display: Rendering instructions screen display...")

        self.bg_canvas = ctk.CTkCanvas(self.main_panel, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.main_panel.update_idletasks()
        self.home_bg_photo = load_bg_image_for_canvas(
            screen=INSTRUCTIONS_SCREEN,
            assets_path="assets/instructions_bg.jpg",
            size=(self.main_panel.winfo_width(), self.main_panel.winfo_height()),
            opacity=0.35,
        )
        self.bg_canvas.create_image(0, 0, anchor="nw", image=self.home_bg_photo)

        ctk.CTkLabel(
            self.bg_canvas,
            text="Game Rules",
            width=500,
            font=ctk.CTkFont(family="Times New Roman", size=42, weight="bold"),
            text_color=ORANGE,
            bg_color=BLACK,
            fg_color=BLACK,
        ).pack(pady=20)

        box = ctk.CTkTextbox(
            self.bg_canvas,
            width=900,
            height=520,
            fg_color=BLACK,
            bg_color=BLACK,
            text_color=PURPLE,
            font=ctk.CTkFont(family="Times New Roman", size=22),
            border_width=2,
            border_color=ORANGE,
            corner_radius=8,
        )
        box.pack(pady=12, padx=8)
        box.insert("end", GAME_INSTRUCTIONS)
        box.configure(state="disabled")

        ctk.CTkButton(
            self.bg_canvas,
            text="BACK",
            width=150,
            bg_color=BLACK,
            fg_color=BLACK,
            command=lambda: self._go_to_home_screen(
                event="BACK", screen="Instructions"
            ),
        ).pack(pady=20)
        logger.info("UI Display: Loaded instructions screen content area.")

        logger.info("UI Display: Completed rendering instructions screen display.")
        logger.info("UI Display: Displaying instructions screen.")

    # <<<

    # >>>
    def _display_choose_task_screen(self):
        logger.info("UI Display: Rendering choose task screen display...")

        self.bg_canvas = ctk.CTkCanvas(self.main_panel, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.main_panel.update_idletasks()
        self.home_bg_photo = load_bg_image_for_canvas(
            screen=CHOOSE_TASK_SCREEN,
            assets_path="assets/task_bg.jpg",
            size=(self.main_panel.winfo_width(), self.main_panel.winfo_height()),
            opacity=0.35,
        )
        self.bg_canvas.create_image(0, 0, anchor="nw", image=self.home_bg_photo)

        content = ctk.CTkFrame(
            self.bg_canvas,
            width=600,
            height=250,
            bg_color=BLACK,
            fg_color=BLACK,
        )
        content.place(relx=0.5, rely=0.5, anchor="center")
        content.pack_propagate(False)

        ctk.CTkLabel(
            content,
            text="What do you want to do first?",
            text_color=ORANGE,
            font=("Times New Roman", 42, "bold"),
        ).pack(pady=40)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack()
        ctk.CTkButton(
            btn_frame,
            text=SET_CODE,
            width=140,
            fg_color=BLUE,
            command=lambda: self._handle_user_taskscreen_choice(SET_CODE),
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            btn_frame,
            text=DE_CODE,
            width=140,
            fg_color=RED,
            hover_color="#D60000",
            command=lambda: self._handle_user_taskscreen_choice(DE_CODE),
        ).pack(side="left", padx=20)
        logger.info("UI Display: Loaded choose task screen content area.")

        logger.info("UI Display: Completed rendering choose task screen display.")
        logger.info("UI Display: Displaying choose task screen.")

    # <<<

    # >>>
    def _display_gameplay_load_screen(self, message):
        logger.info("UI Display: Rendering gameplay load screen display...")

        ctk.CTkLabel(
            self.main_panel,
            text=message,
            font=("Times New Roman", 42, "bold"),
            text_color=ORANGE,
        ).pack(pady=100)

        ctk.CTkLabel(
            self.main_panel,
            text="Loading Game...",
            font=("Times New Roman", 24),
            text_color=WHITE,
        ).place(relx=0.5, rely=0.5, anchor="center")

        logger.info("UI Display: Completed rendering gameplay load screen display.")
        logger.info("UI Display: Displaying gameplay load screen.")

        self.after(5000, self._go_to_gameplay_screen)

    # <<<

    # >>>
    def _display_gameplay_screen(self):
        logger.info("UI Display: Rendering gameplay screen display...")

        gameplay_frame = ctk.CTkFrame(self.main_panel)
        gameplay_frame.pack(fill="both", expand=True)

        # Screen A – Left Panel
        logger.info("UI Display: Creating left panel (screen A) on gameplay screen...")
        screen_a = ctk.CTkFrame(gameplay_frame, width=180, fg_color=ORANGE)
        screen_a.pack(side="left", fill="y", padx=5)
        screen_a.pack_propagate(False)

        self.screen_a_upper_text = ctk.CTkLabel(
            screen_a,
            text="-",
            font=("Times New Roman", 16, "bold"),
            text_color=WHITE,
        )
        self.screen_a_upper_text.pack(pady=5)
        self.screen_a_upper_label = ctk.CTkLabel(
            screen_a,
            text="-",
            font=ctk.CTkFont(size=48),
            text_color=WHITE,
        )
        self.screen_a_upper_label.pack(side="top", pady=5)

        self.start_gameplay_btn = ctk.CTkButton(
            screen_a,
            text="START ▶",
            width=150,
            height=60,
            fg_color=BLACK,
            font=("Times New Roman", 30, "bold"),
            text_color=WHITE,
            command=self._handle_gameplay_flow,
        )
        self.start_gameplay_btn.pack(pady=210)

        self.screen_a_lower_label = ctk.CTkLabel(
            screen_a,
            text="-",
            font=ctk.CTkFont(size=48),
            text_color=WHITE,
        )
        self.screen_a_lower_label.pack(side="bottom", pady=5)
        self.screen_a_lower_text = ctk.CTkLabel(
            screen_a, text="-", font=("Times New Roman", 16, "bold")
        )
        self.screen_a_lower_text.pack(side="bottom", pady=5)

        if self.initial_user_role == SET_CODE:
            self.screen_a_upper_text.configure(text=USER)
            self.screen_a_upper_label.configure(text=SCREEN_A_USER_LABEL)
            self.screen_a_lower_label.configure(text=SCREEN_A_SYSTEM_LABEL)
            self.screen_a_lower_text.configure(text=SYSTEM)
        elif self.initial_user_role == DE_CODE:
            self.screen_a_upper_text.configure(text=SYSTEM)
            self.screen_a_upper_label.configure(text=SCREEN_A_SYSTEM_LABEL)
            self.screen_a_lower_label.configure(text=SCREEN_A_USER_LABEL)
            self.screen_a_lower_text.configure(text=USER)
        logger.info(
            "UI Display: Completed rendering the left panel (screen A) on gameplay screen."
        )

        # Screen B – Center Board
        logger.info(
            "UI Display: Creating center board (screen B) on gameplay screen..."
        )
        self.screen_b = ctk.CTkFrame(gameplay_frame)
        self.screen_b.pack(side="left", fill="both", expand=True, padx=5)

        if self.initial_user_role == SET_CODE:
            self._build_screen_b_board(parent=self.screen_b, current_decoder=SYSTEM)
        elif self.initial_user_role == DE_CODE:
            self._build_screen_b_board(parent=self.screen_b, current_decoder=USER)
        logger.info(
            "UI Display: Completed rendering the center board (screen B) on gameplay screen."
        )

        # Screen C – Right Panel
        logger.info("UI Display: Creating right panel (screen C) on gameplay screen...")
        screen_c = ctk.CTkFrame(gameplay_frame, width=400)
        screen_c.pack(side="right", fill="y", padx=5)
        screen_c.pack_propagate(False)

        ctk.CTkLabel(
            screen_c,
            text="REVEAL • CHAT • ROAST",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        self.chat_scroll = ctk.CTkScrollableFrame(screen_c)
        self.chat_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self._add_chat_message(sender=SYSTEM, message=SYSTEM_WELCOME_TEXT)

        if self.initial_user_role == SET_CODE:
            self._add_chat_message(
                sender=SYSTEM,
                message=SYSTEM_START_GAME_TEXT_FOR_SYSTEM_DECODE,
            )
        elif self.initial_user_role == DE_CODE:
            self._add_chat_message(
                sender=SYSTEM,
                message=SYSTEM_START_GAME_TEXT_FOR_USER_DECODE,
            )

        ctk.CTkButton(
            screen_c,
            text="EXIT ▶",
            width=220,
            height=60,
            fg_color=BLACK,
            font=("Times New Roman", 30, "bold"),
            command=lambda: self._go_to_home_screen(event="EXIT ▶", screen="Gameplay"),
        ).pack(pady=10)
        logger.info(
            "UI Display: Completed rendering the right panel (screen C) on gameplay screen."
        )

        self._add_chat_message(sender=SYSTEM, message=SYSTEM_EXIT_WARNING)
        self._add_chat_message(sender=USER, message=USER_START_TEXT)

        logger.info("UI Display: Completed rendering gameplay screen display.")
        logger.info("UI Display: Displaying gameplay screen.")

    # <<<

    # ==================================================
    # UI - Screen Display Handlers
    # ==================================================
    # >>>
    def _clear_main_panel(self):
        for widget in self.main_panel.winfo_children():
            widget.destroy()
        logger.info("UI Handler: Cleared the Main Panel area.")

    # <<<

    # >>>
    def _reset_app_state_variables(self):

        self.initial_user_role = None
        self.current_user_role = None
        self.current_system_role = None

        self.user_code = []
        self.user_current_guess = None
        self.system_code = []
        self.system_current_guess = None
        self.is_systems_code_revealed = False
        self.system_decoder = SystemDecoder()

        self.current_turn = 0
        self.user_total_turns = 0
        self.system_total_turns = 0

        self.turn_labels = dict()
        self.system_slots = dict()
        self.user_slots = dict()
        self.feedback_labels = dict()

        self.active_color_menu = None

        logger.info("UI Handler: Completed resetting the App-State Variables.")

    # <<<

    # >>>
    def _go_to_home_screen(self, event="", screen=""):
        logger.info("---")

        if (event != None and event != "") and (screen != None and screen != ""):
            logger.info(
                f"UI Handler: User has clicked the {event} button on {screen} screen"
                + "to navigate to home screen."
            )

        logger.info("UI Handler: Handling home screen display >>>")

        self._clear_main_panel()

        self._reset_app_state_variables()

        self.after(1000, self._display_home_screen())

        logger.info("UI Handler: Completed handling home screen display <<<")
        logger.info("---")

    # <<<

    # >>>
    def _go_to_instructions_screen(self):
        logger.info("---")
        logger.info(
            "UI Handler: User has clicked the 'READ INSTRUCTIONS' button on home screen."
        )

        logger.info("UI Handler: Handling instructions screen display >>>")

        self._clear_main_panel()

        self.after(2000, self._display_instructions_screen())

        logger.info("UI Handler: Completed handling instructions screen display <<<")
        logger.info("---")

    # <<<

    # >>>
    def _go_to_choose_task_screen(self):
        logger.info("---")
        logger.info(
            "UI Handler: User has clicked the 'NEW GAME' button on home screen."
        )

        logger.info("UI Handler: Handling choose task screen display >>>")

        self._clear_main_panel()

        self.after(1000, self._display_choose_task_screen())

        logger.info("UI Handler: Completed handling choose task screen display <<<")
        logger.info("---")

    # <<<

    # >>>
    def _handle_user_taskscreen_choice(self, user_choice):

        self.initial_user_role = user_choice
        self.current_user_role = user_choice
        self.current_system_role = (
            SET_CODE if self.current_user_role == DE_CODE else DE_CODE
        )
        logger.info(
            f"UI Handler: User has selected {user_choice} option on choose task screen."
        )
        logger.info(
            f"UI Handler: User's Role: {self.current_user_role}"
            + f" | System's Role: {self.current_system_role}"
        )

        if user_choice == SET_CODE:
            display_text = "You have chosen to SET-CODE first.\nGood Luck."
        elif user_choice == DE_CODE:
            display_text = "You have chosen to DE-CODE first.\nGood Luck."

        self._go_to_gameplay_load_screen(message=display_text)

    # <<<

    # >>>
    def _go_to_gameplay_load_screen(self, message):
        logger.info("---")
        logger.info("UI Handler: Handling gameplay load screen display >>>")

        self._clear_main_panel()

        self._display_gameplay_load_screen(message)

        logger.info("UI Handler: Completed handling gameplay load screen display <<<")
        logger.info("---")

    # <<<

    # >>>
    def _go_to_gameplay_screen(self):
        logger.info("---")
        logger.info("UI Handler: Handling gameplay screen display >>>")

        self._clear_main_panel()

        self._display_gameplay_screen()

        logger.info("UI Handler: Completed handling gameplay screen display <<<")
        logger.info("---")

    # <<<

    # ==================================================
    # UI - Gameplay Board Display
    # ==================================================
    # >>>
    def _build_screen_b_board(self, parent, current_decoder):
        logger.info(
            f"UI Display: Rendering the Screen-B Board for current decoder: {current_decoder}..."
        )

        board = ctk.CTkFrame(parent, fg_color=BLACK)
        board.pack(fill="both", expand=True)
        board.pack_propagate(False)
        board.grid_rowconfigure(0, weight=0)
        board.grid_rowconfigure(1, weight=1)
        board.grid_columnconfigure(0, weight=1)

        logger.info(
            "UI Display: Creating the header frame in Screen-B for current code-setter..."
        )
        # Header Frame
        header_frame = ctk.CTkFrame(board, fg_color=BLACK, height=150)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure((0, 1, 2), weight=0)
        header_frame.pack_propagate(False)

        ## Header Frame - Turn Column
        turn_column_header = ctk.CTkFrame(header_frame, width=120, fg_color=BLACK)
        turn_column_header.pack(side="left", fill="y", padx=1)
        turn_column_header.pack_propagate(False)
        self._create_turn_labels_row(
            parent=turn_column_header, turn_label_text="TURN ▼"
        )

        ## Header Frame - Slots Column
        slots_column_header = ctk.CTkFrame(header_frame, fg_color=BLACK)
        slots_column_header.pack(side="left", fill="both", expand=True, padx=1)
        self._create_peg_slot_row(
            parent=slots_column_header,
            decoder=current_decoder,
            is_header=True,
        )

        ## Header Frame - Feedback Column
        feedback_column_header = ctk.CTkFrame(header_frame, width=170, fg_color=BLACK)
        feedback_column_header.pack(side="left", fill="y", padx=1)
        feedback_column_header.pack_propagate(False)
        self._create_feedback_row(feedback_column_header, feedback="FEEDBACK ▼")
        logger.info(
            "UI Display: Created the header frame in Screen-B for current code-setter."
        )

        # Rows Frame
        self.rows_frame = ctk.CTkScrollableFrame(board, fg_color=BLACK)
        self.rows_frame.grid(row=1, column=0, sticky="nsew")
        self.rows_frame.grid_columnconfigure(1, weight=1)

        logger.info(
            "UI Display: Completed rendering Screen-B Board for the current decoder."
        )

    # <<<

    # >>>
    def _create_turn_labels_row(self, parent, turn_num=None, turn_label_text="-"):

        turn_label_row = ctk.CTkFrame(parent, height=32)
        turn_label_row.pack(fill="both", expand=True, padx=10, pady=10)

        turn_label = ctk.CTkLabel(
            turn_label_row,
            text=turn_label_text,
            width=80,
            font=("Times New Roman", 16, "bold"),
            anchor="center",
        )
        turn_label.place(relx=0.5, rely=0.5, anchor="center")
        turn_label.pack_propagate(False)

        if turn_num != None:
            self.turn_labels[turn_num] = turn_label
            logger.info(f"UI Display: Created turn-label for turn number: {turn_num}")
        else:
            logger.info("UI Display: Created turn-label for Header.")

    # <<<

    # >>>
    def _create_peg_slot_row(
        self,
        parent,
        decoder,
        is_header=False,
    ):

        slot = ctk.CTkFrame(parent, height=32)
        slot.pack(fill="both", expand=True, padx=10, pady=10)

        slot_buttons = {
            BTN1: None,
            BTN2: None,
            BTN3: None,
            BTN4: None,
            BTN5: None,
            ADD_BTN: None,
        }

        # Case: System's Header Peg Slot when user is decoding
        if is_header and decoder == USER:

            ctk.CTkLabel(
                slot,
                text="SYSTEM's SECRET CODE",
                text_color=WHITE,
                font=("Times New Roman", 16, "bold"),
            ).pack()

            for btn_num in range(1, 6):
                btn = ctk.CTkButton(
                    slot,
                    text="",
                    width=30,
                    height=30,
                    fg_color="gray",
                    corner_radius=14,
                    state="disabled",
                )
                btn.pack(side="left", padx=10)
                slot_buttons["btn" + str(btn_num)] = btn

            additional_btn = ctk.CTkButton(
                slot,
                text=ADD_BTN_HEADER_TEXTS[decoder],
                width=30,
                height=30,
                state="disabled",
                command=self._execute_reveal_system_code,
            )
            additional_btn.pack(side="left", padx=40)

            slot_buttons[ADD_BTN] = additional_btn
            self.system_slots[HEADER_SLOT] = slot_buttons
            logger.info("UI Display: Created Header Peg Slot Row for system.")

        # Case: User's Header Peg Slot when system is decoding
        if is_header and decoder == SYSTEM:

            ctk.CTkLabel(
                slot,
                text="YOUR SECRET CODE",
                text_color=WHITE,
                font=("Times New Roman", 16, "bold"),
            ).pack()

            for btn_num in range(1, 6):
                btn = ctk.CTkButton(
                    slot,
                    text="",
                    width=30,
                    height=30,
                    fg_color="gray",
                    corner_radius=14,
                    state="disabled",
                )
                btn.pack(side="left", padx=10)
                slot_buttons["btn" + str(btn_num)] = btn

            additional_btn = ctk.CTkButton(
                slot,
                text=ADD_BTN_HEADER_TEXTS[decoder],
                width=30,
                height=30,
                state="disabled",
            )
            additional_btn.pack(side="left", padx=40)

            slot_buttons[ADD_BTN] = additional_btn
            self.user_slots[HEADER_SLOT] = slot_buttons
            logger.info("UI Display: Created Header Peg Slot Row for user.")

        if not is_header:
            for btn_num in range(1, 6):
                btn = ctk.CTkButton(
                    slot,
                    text="",
                    width=30,
                    height=30,
                    fg_color="gray",
                    corner_radius=14,
                    state="disabled",
                )
                btn.pack(side="left", padx=10)
                slot_buttons["btn" + str(btn_num)] = btn

            additional_btn = ctk.CTkButton(
                slot,
                text="VALIDATE CODE ▶",
                width=30,
                height=30,
                state="disabled",
            )
            additional_btn.pack(side="left", padx=35)
            slot_buttons[ADD_BTN] = additional_btn

            if decoder == USER:
                self.user_slots[self.current_turn] = slot_buttons
                logger.info(
                    "UI Display: Created normal peg slot row for user's decoding turn."
                )
            elif decoder == SYSTEM:
                self.system_slots[self.current_turn] = slot_buttons
                logger.info(
                    "UI Display: Created normal peg slot row for system's decoding turn."
                )

    # <<<

    # >>>
    def _create_feedback_row(self, parent, turn_num=None, feedback="⚪⚪⚪⚪⚪"):

        feedback_row = ctk.CTkFrame(parent, height=32)
        feedback_row.pack(fill="both", expand=True, padx=10, pady=10)

        feedback_label = ctk.CTkLabel(
            feedback_row,
            text=feedback,
            width=80,
            font=("Times New Roman", 16, "bold"),
            anchor="w",
        )
        feedback_label.place(relx=0.5, rely=0.5, anchor="center")
        feedback_label.pack_propagate(False)

        if turn_num != None:
            self.feedback_labels[turn_num] = feedback_label
            logger.info(
                f"UI Display: Created feedback-label for turn number: {turn_num}"
            )
        else:
            logger.info("UI Display: Created turn-label for Header.")

    # <<<

    # >>>
    def _create_full_tlpsf_row(self, decoder):

        logger.info(
            f"UI Display: Creating TLPSF Row for current decoder: {decoder}"
            + f" for current turn: {self.current_turn}..."
        )

        # TLSF Row Frame: Turn Labels + Peg Slots + Feedback Row Frame
        tlpsf_row_frame = ctk.CTkFrame(self.rows_frame, fg_color=BLACK, height=120)
        tlpsf_row_frame.pack(fill="x", padx=0, pady=2)
        tlpsf_row_frame.pack_propagate(False)

        ## TLSF Row Frame - Turn Column
        turn_column = ctk.CTkFrame(tlpsf_row_frame, width=115, fg_color=BLACK)
        turn_column.pack(side="left", fill="y", padx=0)
        turn_column.pack_propagate(False)
        self._create_turn_labels_row(
            parent=turn_column,
            turn_num=self.current_turn,
            turn_label_text=str(self.current_turn),
        )

        ## TLSF Row Frame - Slots Column
        slots_column = ctk.CTkFrame(tlpsf_row_frame, fg_color=BLACK)
        slots_column.pack(side="left", fill="both", expand=True, padx=1)
        self._create_peg_slot_row(parent=slots_column, decoder=decoder)

        ## TLSF Row Frame - Feedback Column
        feedback_column = ctk.CTkFrame(tlpsf_row_frame, width=200, fg_color=BLACK)
        feedback_column.pack(side="left", fill="y", padx=0)
        feedback_column.pack_propagate(False)
        self._create_feedback_row(parent=feedback_column, turn_num=self.current_turn)

        logger.info(
            f"UI Display: Created TLPSF Row for current decoder: {decoder}"
            + f" for current turn: {self.current_turn}"
        )

    # <<<

    # >>>
    def _add_chat_message(self, sender, message):

        logger.info("UI Display: Creating chat message for Screen-C >>>")
        chat_frame = ctk.CTkFrame(
            self.chat_scroll, fg_color=BLACK, corner_radius=10, width=350
        )
        chat_frame.pack(padx=5, pady=5)
        chat_frame.pack_propagate(False)

        sender_label = ctk.CTkLabel(
            chat_frame,
            text=sender,
            font=("Times New Roman", 22, "bold"),
            text_color=ORANGE if sender == "SYSTEM" else BLUE,
            anchor="center",
        )
        sender_label.pack(fill="x", pady=(6, 2))

        divider = ctk.CTkFrame(
            chat_frame,
            height=1,
            fg_color="gray",
        )
        divider.pack(fill="x", padx=8, pady=(0, 6))
        divider.pack_propagate(False)

        message_label = ctk.CTkLabel(
            chat_frame,
            text=message,
            font=("Times New Roman", 18),
            wraplength=334,
            justify="left",
            anchor="w",
            text_color=ORANGE if sender == "SYSTEM" else BLUE,
        )
        message_label.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        logger.info(f"UI Display: Sender: {sender} | Message: {message}")
        logger.info("UI Display: Completed creating chat message in Screen-C <<<")

    # <<<

    # ==================================================
    # Gameplay Board Display Handlers
    # ==================================================
    # >>>
    def _clear_gameplay_screen_b_board(self):
        logger.info("UI Handler: Clearing all widgets in Screen-B Board...")
        for widget in self.screen_b.winfo_children():
            widget.destroy()
        logger.info("UI Handler: Completed clearing Screen-B Board.")

    # <<<

    # >>>
    def _swap_screen_a_labels(self):

        logger.info("UI Handler: Swapping 'USER' and 'SYSTEM' labels on Screen-A...")

        if self.initial_user_role == DE_CODE:
            self.screen_a_upper_text.configure(text=USER)
            self.screen_a_upper_label.configure(text=SCREEN_A_USER_LABEL)
            self.screen_a_lower_label.configure(text=SCREEN_A_SYSTEM_LABEL)
            self.screen_a_lower_text.configure(text=SYSTEM)

        elif self.initial_user_role == SET_CODE:
            self.screen_a_upper_text.configure(text=SYSTEM)
            self.screen_a_upper_label.configure(text=SCREEN_A_SYSTEM_LABEL)
            self.screen_a_lower_label.configure(text=SCREEN_A_USER_LABEL)
            self.screen_a_lower_text.configure(text=USER)

        logger.info(
            "UI Handler: Completed swapping 'USER' and 'SYSTEM' labels on Screen-A."
        )

    # <<<

    # >>>
    def _enable_reveal_system_code(self):
        self.system_slots[HEADER_SLOT][ADD_BTN].configure(state="normal")
        logger.info("UI Handler: Enabling System-Header 'REVEAL CODE' button. ")

    # <<<

    # ==================================================
    # Gameflow Handlers
    # ==================================================
    # >>>
    def _handle_gameplay_flow(self):
        logger.info("---")
        logger.info("Gameflow Handler: Handling gameplay flow...")

        logger.info(f"Gameflow Handler: Current User Role: {self.current_user_role}")
        logger.info(
            f"Gameflow Handler: Current System Role: {self.current_system_role}"
        )

        if self.current_user_role == DE_CODE:
            logger.info("Gameflow Handler: Starting user decode game.")
            self._start_user_decode_game()
        elif self.current_user_role == SET_CODE:
            logger.info("Gameflow Handler: Starting system decode game.")
            self._start_system_decode_game()

        logger.info("Gameflow Handler: Completed handling gameplay flow.")
        logger.info("---")

    # <<<

    # >>>
    def _start_user_decode_game(self):
        logger.info(
            "Gameflow Handler: Handling User's start decode | System's start set-code game..."
        )

        self.start_gameplay_btn.configure(state="disabled")
        logger.info(
            "Gameflow Handler: Disabled the 'START' gameplay button on Screen-A."
        )

        self._set_code_for_system()
        self._add_chat_message(sender=SYSTEM, message=SYSTEM_SET_CODE_TEXT)

        self._enable_reveal_system_code()
        self._add_chat_message(sender=SYSTEM, message=SYSTEM_REVEAL_CODE_WARNING_TEXT)
        self._add_chat_message(sender=USER, message=USER_SET_CODE_TEXT_REPLY)

        self.current_turn = 1
        self._activate_user_turn()
        logger.info(
            "Gameflow Handler: Completed handling User's start decode | System's start set-code game."
        )

    # <<<

    # >>>
    def _start_system_decode_game(self):
        logger.info(
            "Gameflow Handler: Handling User's start set-code | System's start decode game..."
        )

        self.start_gameplay_btn.configure(state="disabled")
        logger.info(
            "Gameflow Handler: Disabled the 'START' gameplay button on Screen-A."
        )

        self._set_code_for_user()
        self._add_chat_message(
            sender=SYSTEM, message=SYSTEM_PROMPT_USER_TO_SET_CODE_TEXT
        )
        self._add_chat_message(sender=USER, message=USER_PROMPT_SYSTEM_TO_DECODE)

        logger.info(
            "Gameflow Handler: Completed handling User's start set-code | System's start decode game."
        )

    # <<<

    # >>>
    def _handle_gameplay_transition(self):
        logger.info("---")
        logger.info("Gameflow Handler: Handling gameplay transition...")

        self._refresh_gameplay_variables()

        logger.info(f"Gameflow Handler: User's {self.initial_user_role} role complete.")
        if self.initial_user_role == DE_CODE:
            logger.info(
                "Gameflow Handler: Turns taken by User to crack System's Code: "
                + f"{self.user_total_turns}"
            )
        elif self.initial_user_role == SET_CODE:
            logger.info(
                "Gameflow Handler: Turns taken by System to crack User's Code: "
                + f"{self.system_total_turns}"
            )

        self._clear_gameplay_screen_b_board()

        self._swap_screen_a_labels()

        if self.initial_user_role == DE_CODE:
            self.current_user_role = SET_CODE
            self.current_system_role = DE_CODE
            logger.info(
                f"Gameflow Handler: User's next role: {self.current_user_role}."
            )
            self._build_screen_b_board(parent=self.screen_b, current_decoder=SYSTEM)
            self.start_gameplay_btn.configure(
                text="SET ▶", state="normal", command=self._handle_gameplay_flow
            )

        elif self.initial_user_role == SET_CODE:
            self.current_user_role = DE_CODE
            self.current_system_role = SET_CODE
            logger.info(
                f"Gameflow Handler: User's next role: {self.current_user_role}."
            )
            self._build_screen_b_board(parent=self.screen_b, current_decoder=USER)
            self.start_gameplay_btn.configure(
                text="START ▶", state="normal", command=self._handle_gameplay_flow
            )

        logger.info("Gameflow Handler: Completed handling gameplay transition.")
        logger.info("---")

    # <<<

    # >>>
    def _refresh_gameplay_variables(self):

        self.system_code = []
        self.system_current_guess = None
        self.is_systems_code_revealed = False
        self.system_decoder = SystemDecoder()

        self.user_code = []
        self.user_current_guess = None

        self.current_turn = 0

        self.turn_labels = dict()
        self.system_slots = dict()
        self.user_slots = dict()
        self.feedback_labels = dict()

        self.active_color_menu = None

        logger.info("Gameflow Handler: Completed refreshing gameplay variables.")

    # <<<

    # >>>
    def _handle_gameplay_ending(self):
        logger.info("---")
        logger.info("Gameflow Handler: Handling gameplay ending...")

        if self.is_systems_code_revealed == True:

            logger.info(f"System Slots: {self.system_slots[HEADER_SLOT]}")

            self.system_slots[HEADER_SLOT][ADD_BTN].configure(state="disabled")
            logger.info("Gameflow Handler: Disabled the 'REVEAL CODE' button.")

            self.start_gameplay_btn.configure(state="disabled")
            logger.info("Gameflow Handler: Disabled the 'START' gameplay button.")

            self._disable_row_peg_slot_buttons(decoder=USER)

            self._add_chat_message(
                sender=SYSTEM, message=SYSTEM_REPLY_TO_USER_REVEAL_CODE_TEXT
            )
            self._add_chat_message(sender=USER, message=USER_REVEAL_CODE_REPLY)

            logger.info("Gameflow Handler: Declared the SYSTEM as WINNER.")
            logger.info("Gameflow Handler: GAME ENDED.")
            return

        logger.info(
            f"Gameplay Handler: Turns taken by User to crack System's Code: {self.user_total_turns}"
        )
        logger.info(
            f"Gameplay Handler: Turns taken by System to crack User's Code: {self.system_total_turns}"
        )

        if self.user_total_turns > self.system_total_turns:
            logger.info("Gameplay Handler: System won the game!")
            self._add_chat_message(
                sender=SYSTEM,
                message=f"Turns taken by you to crack my code: {self.user_total_turns}\n\n"
                + f"Turns taken by me to crack your code: {self.system_total_turns}",
            )
            self._add_chat_message(sender=SYSTEM, message=SYSTEM_WINNING_TEXT)

        elif self.user_total_turns < self.system_total_turns:
            logger.info("Gameplay Handler: User won the game!")
            self._add_chat_message(
                sender=USER,
                message=f"Turns taken by you to crack my code: {self.system_total_turns}\n\n"
                + f"Turns taken by me to crack your code: {self.user_total_turns}",
            )
            self._add_chat_message(sender=USER, message=USER_WINNING_TEXT)

        else:
            logger.info("Gameplay Handler: Game ended in a tie!.")
            self._add_chat_message(
                sender=SYSTEM,
                message=f"Turns taken by you to crack my code: {self.user_total_turns}\n\n"
                + f"Turns taken by me to crack your code: {self.system_total_turns}",
            )
            self._add_chat_message(sender=SYSTEM, message=SYSTEM_TIE_TEXT)

        self._add_chat_message(sender=SYSTEM, message=SYSTEM_EXIT_TEXT)
        logger.info("Gameflow Handler: Completed handling gameplay ending.")
        logger.info("---")

    # <<<

    # ==================================================
    # System Gameplay Handlers - System's Role: SET-CODE
    # ==================================================
    # >>>
    def _set_code_for_system(self):
        self.system_code = create_colour_code()
        logger.info(
            f"System Gameplay: System has set {self.system_code} as the code for user to crack."
        )

    # <<<

    # >>>
    def _handle_system_code_after_user_decode(self):

        logger.info("System Gameplay: User has cracked the system's code.")

        for i in range(CODE_LENGTH):
            self.system_slots[HEADER_SLOT]["btn" + str(i + 1)].configure(
                fg_color=self.system_code[i]
            )
        logger.info(f"System Gameplay: Displayed the System's Code: {self.system_code}")

        self.system_slots[HEADER_SLOT][ADD_BTN].configure(state="disabled")
        logger.info(
            "System Gameplay: Disabled the additional button in the System's Header slot."
        )

        logger.info(
            "System Gameplay: Completed handling system code after user decode."
        )

    # <<<

    # ==================================================
    # System Gameplay Handlers - System's Role: DECODE
    # ==================================================
    # >>>
    def _activate_system_turn(self):

        logger.info(
            f"System Gameplay: Activating System's turn. Turn Number: {self.current_turn}"
        )
        self._create_full_tlpsf_row(decoder=SYSTEM)

        logger.info(f"System Gameplay: Code set by user is {self.user_code}")
        self._fill_row_with_system_guess()

    # <<<

    # >>>
    def _fill_row_with_system_guess(self):

        logger.info("System Gameplay: Filling the current row with system's guess...")

        if self.current_turn == 1:
            self._generate_systems_first_guess()
        else:
            self._generate_systems_next_guess()

        slot_btns = self.system_slots[self.current_turn]

        for i in range(CODE_LENGTH):
            slot_btns[f"btn{i+1}"].configure(
                fg_color=self.system_current_guess[i], state="disabled"
            )

        logger.info(
            f"System Gameplay: Current Turn: {self.current_turn}"
            + f"| System's Guess: {self.system_current_guess}"
        )

        slot_btns[ADD_BTN].configure(
            state="normal", command=self._execute_validate_code_for_system_decode
        )
        logger.info(
            "System Gameplay: Enabled the 'VALIDATE CODE' button for colour validation."
        )
        logger.info(
            "System Gameplay: Completed filling the current row with system's guess."
        )

    # <<<

    # >>>
    def _generate_systems_first_guess(self):

        self.system_current_guess = self.system_decoder.generate_guess()

        self.system_code.append(self.system_current_guess)

        logger.info(
            f"System Gameplay: Generated system's first guess: {self.system_current_guess}"
        )

    # <<<

    # >>>
    def _generate_systems_next_guess(self):

        self.system_current_guess = self.system_decoder.generate_guess()

        self.system_code.append(self.system_current_guess)

        logger.info(
            f"System Gameplay: Generated system's next guess: {self.system_current_guess}"
        )

    # <<<

    # ==================================================
    # User Gameplay Handlers - User's Role: DECODE
    # ==================================================
    # >>>
    def _execute_reveal_system_code(self):

        logger.info(
            "User Gameplay: User has clicked the System's 'REVEAL CODE' button."
        )
        self.is_systems_code_revealed = True

        for i in range(CODE_LENGTH):
            self.system_slots[HEADER_SLOT]["btn" + str(i + 1)].configure(
                fg_color=self.system_code[i]
            )
        logger.info(f"User Gameplay: Revealed the System's Code: {self.system_code}")

        self._handle_gameplay_ending()

    # <<<

    # >>>
    def _activate_user_turn(self):

        logger.info(
            f"User Gameplay: Activating User's turn. Turn Number: {self.current_turn}"
        )
        self._create_full_tlpsf_row(decoder=USER)

        logger.info(f"User Gameplay: Code set by system: {self.system_code}")
        self._enable_row_peg_slot_buttons()

    # <<<

    # >>>
    def _enable_row_peg_slot_buttons(self):

        logger.info("User Gameplay: Enabling User's peg slot buttons...")

        slot_btns = self.user_slots[self.current_turn]

        for i in range(1, 6):
            btn = slot_btns[f"btn{i}"]
            btn.configure(
                state="normal",
                command=lambda b=btn, p=i: self._open_colour_dropdown(b, p),
            )

        logger.info(
            f"User Gameplay: Enabled User's peg slot buttons for turn: {self.current_turn}"
        )

    # <<<

    # >>>
    def _open_colour_dropdown(self, button, peg):

        logger.info(
            f"User Gameplay: User has opened the colour dropdown on Peg-{peg} in the current slot."
        )

        if self.active_color_menu is not None:
            self.active_color_menu.destroy()
            self.active_color_menu = None

        menu = ctk.CTkOptionMenu(
            master=button.master,
            values=COLOUR_OPTIONS,
            command=lambda color, b=button, p=peg: self._set_peg_color(b, p, color),
            width=120,
        )

        menu.place(x=button.winfo_x(), y=button.winfo_y() + button.winfo_height() + 4)

        self.active_color_menu = menu

    # <<<

    # >>>
    def _set_peg_color(self, button, peg, color_name):

        button.configure(fg_color=COLOUR_MAP[color_name])
        logger.info(
            f"User Gameplay: User has set {color_name} colour in Peg-{peg} in the current slot."
        )

        if self.active_color_menu is not None:
            self.active_color_menu.destroy()
            self.active_color_menu = None

        self._check_if_slot_is_filled()

    # <<<

    # >>>
    def _check_if_slot_is_filled(self):

        logger.info("User Gameplay: Checking if current slot is filled...")

        slot_btns = self.user_slots[self.current_turn]
        slot_btn_colours = []
        slot_filled = False

        for i in range(1, 6):

            if slot_btns[f"btn{i}"].cget("fg_color") == "gray":
                slot_filled = False
                logger.info("User Gameplay: Current slot not yet filled fully.")
                break

            slot_btn_colours.append(slot_btns[f"btn{i}"].cget("fg_color"))
            slot_filled = True

        if slot_filled:
            logger.info("User Gameplay: Current slot is filled.")

            logger.info(
                f"User Gameplay: Current Turn: {self.current_turn}"
                + f" | Slot Button Colors filled by user: {slot_btn_colours}"
            )

            self.user_current_guess = slot_btn_colours

            slot_btns[ADD_BTN].configure(
                state="normal", command=self._execute_validate_code_for_user_decode
            )
            logger.info(
                "User Gameplay: Enabled the 'VALIDATE CODE' button for current slot."
            )

    # <<<

    # >>>
    def _disable_row_peg_slot_buttons(self, decoder):

        if decoder == USER:
            logger.info("User Gameplay: Disabling User's peg slot buttons...")
            slot_btns = self.user_slots[self.current_turn]
        elif decoder == SYSTEM:
            logger.info("System Gameplay: Disabling System's peg slot buttons...")
            slot_btns = self.system_slots[self.current_turn]

        for i in range(1, 6):
            slot_btns[f"btn{i}"].configure(state="disabled")

        slot_btns[ADD_BTN].configure(state="disabled")

        if decoder == USER:
            logger.info("User Gameplay: Completed disabling User's peg slot buttons.")
        elif decoder == SYSTEM:
            logger.info(
                "System Gameplay: Completed disabling System's peg slot buttons."
            )

    # <<<

    # ==================================================
    # User Gameplay Handlers - User's Role: SET-CODE
    # ==================================================

    # >>>
    def _set_code_for_user(self):
        self._enable_header_row_peg_slot_buttons()
        logger.info(
            "User Gameplay: Enabled the header row peg slot buttons for user to fill colours."
        )

    # <<<

    # >>>
    def _enable_header_row_peg_slot_buttons(self):

        logger.info("User Gameplay: Enabling User's Header row peg slot buttons...")

        slot_btns = self.user_slots[HEADER_SLOT]

        for i in range(1, 6):
            btn = slot_btns[f"btn{i}"]
            btn.configure(
                state="normal",
                command=lambda b=btn, p=i: self._open_header_pegs_color_dropdown(b, p),
            )

        logger.info("User Gameplay: Enabled User's header row peg slot buttons.")

    # <<<

    # >>>
    def _open_header_pegs_color_dropdown(self, button, peg):

        logger.info(
            f"User Gameplay: User has opened the colour dropdown on Peg-{peg} in the header slot."
        )

        if self.active_color_menu is not None:
            self.active_color_menu.destroy()
            self.active_color_menu = None

        menu = ctk.CTkOptionMenu(
            master=button.master,
            values=COLOUR_OPTIONS,
            command=lambda color, b=button, p=peg: self._set_header_peg_color(
                b, p, color
            ),
            width=120,
        )

        menu.place(x=button.winfo_x(), y=button.winfo_y() + button.winfo_height() + 4)

        self.active_color_menu = menu

    # <<<

    # >>>
    def _set_header_peg_color(self, button, peg, color_name):

        button.configure(fg_color=COLOUR_MAP[color_name])
        logger.info(
            f"User Gameplay: User has set {color_name} colour in Peg-{peg} in the header slot."
        )

        if self.active_color_menu is not None:
            self.active_color_menu.destroy()
            self.active_color_menu = None

        self._check_if_header_slot_is_filled()

    # >>>

    # >>>
    def _check_if_header_slot_is_filled(self):

        logger.info("User Gameplay: Checking if header slot is filled...")

        slot_btns = self.user_slots[HEADER_SLOT]
        slot_btn_colours = []
        slot_filled = False

        for i in range(1, 6):

            if slot_btns[f"btn{i}"].cget("fg_color") == "gray":
                slot_filled = False
                logger.info("User Gameplay: Header slot not yet filled fully.")
                break

            slot_btn_colours.append(slot_btns[f"btn{i}"].cget("fg_color"))
            slot_filled = True

        if slot_filled:
            logger.info("User Gameplay: Header slot is filled.")

            logger.info(
                f"User Gameplay:  User's Header Slot Button Colors: {slot_btn_colours}"
            )

            self.user_code = slot_btn_colours

            slot_btns[ADD_BTN].configure(
                state="normal",
                text="ENCRYPT CODE ▶",
                command=self._encrypt_header_row_peg_slot_buttons,
            )
            logger.info(
                "User Gameplay: Enabled the 'ENCRYPT CODE' button for user's header slot."
            )

    # <<<

    # >>>
    def _encrypt_header_row_peg_slot_buttons(self):

        logger.info("User Gameplay: Encrypting the User's code...")

        slot_btns = self.user_slots[HEADER_SLOT]

        for i in range(1, 6):
            slot_btns[f"btn{i}"].configure(state="disabled", fg_color="gray")

        self._enable_view_user_code()

        logger.info("User Gameplay: Completed encrypting the User's code.")

        self.current_turn = 1
        self._activate_system_turn()

    # <<<

    # >>>
    def _enable_view_user_code(self):

        slot_btns = self.user_slots[HEADER_SLOT]

        slot_btns[ADD_BTN].configure(
            state="normal",
            text="VIEW CODE ▶",
            command=self._view_header_row_peg_slot_colors,
        )

        logger.info("User Gameplay: Enabled 'VIEW CODE' button to view User's Code.")

    # <<<

    # >>>
    def _view_header_row_peg_slot_colors(self):

        logger.info(
            "User Gameplay: User has clicked on 'VIEW CODE' in the header slot."
        )

        slot_btns = self.user_slots[HEADER_SLOT]

        for i in range(5):
            slot_btns[f"btn{i+1}"].configure(
                state="disabled", fg_color=self.user_code[i]
            )

        logger.info("User Gameplay: Displayed User's Set Code to the User.")

        slot_btns[ADD_BTN].configure(
            state="normal",
            text="HIDE CODE ▶",
            command=self._hide_header_row_peg_slot_colors,
        )
        logger.info("User Gameplay: Enabled 'HIDE CODE' button to view User's Code.")

    # <<<

    # >>>
    def _hide_header_row_peg_slot_colors(self):

        logger.info(
            "User Gameplay: User has clicked on 'HIDE CODE' in the header slot."
        )

        slot_btns = self.user_slots[HEADER_SLOT]

        for i in range(1, 6):
            slot_btns[f"btn{i}"].configure(state="disabled", fg_color="gray")

        logger.info("User Gameplay: Encrypted and hid back User's code.")

        slot_btns[ADD_BTN].configure(
            state="normal",
            text="VIEW CODE ▶",
            command=self._view_header_row_peg_slot_colors,
        )
        logger.info("User Gameplay: Enabled 'VIE CODE' button to view User's Code.")

    # <<<

    # >>>
    def _handle_user_code_after_system_decode(self):

        logger.info("User Gameplay: System has cracked the user's code.")

        for i in range(CODE_LENGTH):
            self.user_slots[HEADER_SLOT]["btn" + str(i + 1)].configure(
                fg_color=self.user_code[i]
            )
        logger.info(f"User Gameplay: Displayed the User's Code: {self.user_code}")

        self.user_slots[HEADER_SLOT][ADD_BTN].configure(state="disabled")
        logger.info(
            "User Gameplay: Disabled the additional button in the User's Header slot."
        )

        logger.info("User Gameplay: Completed handling user code after system decode.")

    # <<<

    # ==================================================
    # Gameplay Code Validation Handlers
    # ==================================================
    # >>>
    def _execute_validate_code_for_user_decode(self):

        self.user_code.append(self.user_current_guess)

        self._disable_row_peg_slot_buttons(decoder=USER)

        feedback = evaluate_guess(
            secret=self.system_code, guess=self.user_code[self.current_turn - 1]
        )
        self.feedback_labels[self.current_turn].configure(text=feedback)

        logger.info(
            f"Validation Handler: Turn: {self.current_turn} | Feedback: {feedback}"
        )
        self._add_chat_message(
            sender=SYSTEM,
            message=f"Turn Number: {self.current_turn}\n\nFeedback to your guess: {feedback}",
        )

        if feedback == "✅✅✅✅✅":

            self._handle_system_code_after_user_decode()

            self.user_total_turns = self.current_turn
            logger.info(
                "Validation Handler: Number of turns taken by user to crack the code: "
                + f"{self.user_total_turns}"
            )
            self._add_chat_message(
                sender=SYSTEM, message=SYSTEM_REPLY_TO_USER_CRACKING_CODE
            )

            if self.current_user_role != self.initial_user_role:
                self._handle_gameplay_ending()
                return

            self.start_gameplay_btn.configure(
                text="NEXT ▶",
                state="normal",
                command=self._handle_gameplay_transition,
            )

            self._add_chat_message(sender=SYSTEM, message=SYSTEM_NEXT_PART_TEXT)
            return

        self.current_turn = self.current_turn + 1
        self._activate_user_turn()

    # <<<

    # >>>
    def _execute_validate_code_for_system_decode(self):

        self._disable_row_peg_slot_buttons(decoder=SYSTEM)

        feedback = evaluate_guess(
            secret=self.user_code, guess=self.system_code[self.current_turn - 1]
        )
        self.feedback_labels[self.current_turn].configure(text=feedback)

        logger.info(
            f"Validation Handler: Turn: {self.current_turn} | Feedback: {feedback}"
        )
        self._add_chat_message(
            sender=USER,
            message=f"Turn Number: {self.current_turn}\n\nFeedback to your guess: {feedback}",
        )

        if feedback == "✅✅✅✅✅":

            self._handle_user_code_after_system_decode()

            self.system_total_turns = self.current_turn
            logger.info(
                "Validation Handler: Number of turns taken by system to crack the code: "
                + f"{self.system_total_turns}"
            )
            self._add_chat_message(
                sender=USER, message=USER_REPLY_TO_SYSTEM_CRACKING_CODE
            )

            if self.current_user_role != self.initial_user_role:
                self._handle_gameplay_ending()
                return

            self.start_gameplay_btn.configure(
                text="NEXT ▶",
                state="normal",
                command=self._handle_gameplay_transition,
            )

            self._add_chat_message(sender=SYSTEM, message=SYSTEM_NEXT_PART_TEXT)
            return

        feedback_string = convert_feedback_emojis_to_string(feedback)
        self.system_decoder.update_knowledge(feedback_string)

        self.current_turn = self.current_turn + 1
        self._activate_system_turn()

    # <<<
