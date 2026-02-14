# SuperMastermind: 🔘⚪⚫🟤🟣🔵🟢🟡🟠🔴

import customtkinter as ctk
import logging

from ui.main_window import MainWindow
from ui.background import open_background_app, close_background_app
from util.logging_config import setup_logging
from util.constants import APP_NAME


def main():

    setup_logging()
    logger = logging.getLogger(APP_NAME)
    logger.info("START")
    logger.info("App Logger: Logging configuration is complete.")

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = ctk.CTk()
    app.title(APP_NAME)
    app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
    app.resizable(True, True)

    app.attributes("-alpha", 0.0)
    app.protocol("WM_DELETE_WINDOW", lambda: close_background_app(app))

    open_background_app(app)

    main_window = MainWindow(app)
    main_window.pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()
