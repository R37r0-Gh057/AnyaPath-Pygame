from pathlib import Path

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"

ANYA_DIR = SPRITES_DIR / "anya"

# =========================
# WINDOW
# =========================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FPS = 60
TITLE = "AnyaPath Remastered"

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (18, 18, 18)

PINK = (255, 170, 200)
LIGHT_PINK = (255, 210, 225)

RED = (255, 100, 100)

GREEN = (130, 255, 170)

GRAY = (50, 50, 50)

DIALOGUE_BG = (20, 20, 28)
DIALOGUE_BORDER = (255, 190, 210)

BUTTON_IDLE = (255, 180, 210)
BUTTON_HOVER = (255, 210, 230)

TEXT_PRIMARY = (245, 245, 245)
TEXT_SECONDARY = (200, 200, 200)

TITLE_TEXT = (255, 230, 240)
SUBTITLE_TEXT = (235, 235, 235)

# =========================
# FONTS
# =========================
TITLE_FONT_SIZE = 48
DIALOGUE_FONT_SIZE = 34
BUTTON_FONT_SIZE = 28
MATRIX_FONT_SIZE = 40

# =========================
# UI
# =========================
DIALOGUE_HEIGHT = 180
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60

TYPEWRITER_SPEED = 35  # chars per second

# =========================
# ANIMATION
# =========================
FADE_SPEED = 250
BREATH_SPEED = 2
BREATH_AMOUNT = 8
