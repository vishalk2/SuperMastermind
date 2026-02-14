import logging

from PIL import Image, ImageEnhance, ImageTk

from util.constants import APP_NAME
from util.logics import handle_assets_path

logger = logging.getLogger(APP_NAME)


# >>>
def open_background_app(window):
    logger.info("Background: User has triggered the SuperMastermind.exe application.")
    fade_in(window)
    logger.info("Background: SuperMastermind application has started running.")


def fade_in(window, step=0.02, delay=15):
    alpha = window.attributes("-alpha")
    if alpha < 1.0:
        alpha += step
        window.attributes("-alpha", alpha)
        window.after(delay, fade_in, window, step, delay)


# <<<


# >>>
def close_background_app(window):
    logger.info("Background: User has closed the application.")
    fade_out_and_close(window)
    logger.info("Background: SuperMastermind application has stopped running.")
    logger.info("END")


def fade_out_and_close(window):
    alpha = window.attributes("-alpha")
    if alpha > 0:
        window.attributes("-alpha", alpha - 0.05)
        window.after(15, fade_out_and_close, window)
    else:
        window.destroy()


# <<<


# >>>
def load_bg_image_for_canvas(screen, assets_path, size, opacity=0.4):
    logger.info(f"UI Background: Loading background image for {screen} screen...")

    assets_path = handle_assets_path(relative_path=assets_path)

    image = Image.open(assets_path).resize(size, Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(opacity)

    logger.info(f"UI Background: Loaded background image for {screen} screen.")
    return ImageTk.PhotoImage(image)


# <<<
