import pygame
from game.ui import (
    Button,
    DialogueBox,
    InputField,
    MatrixGrid
)
from constants import (
    ANYA_DIR,
    FPS,
    SPRITES_DIR,
    TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WHITE,
    DIALOGUE_HEIGHT
)
from game.audio import AudioManager
from game.animation import FadeAnimation
from game.state import GameState
from game.word_guesser import WordGuesser


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = GameState.SPLASH

        # Managers
        self.audio = AudioManager()
        self.guesser = WordGuesser()

        # Animation
        self.fade = FadeAnimation()

        # Fonts
        self.title_font = pygame.font.Font(
            None,
            60,
        )

        # Assets
        self.background = self.load_background()
        self.anya_sprites = self.load_anya_sprites()

        self.current_sprite = 0

        self.dialogue_box = DialogueBox(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self.continue_button = Button(
            pygame.Rect(
                WINDOW_WIDTH - 250,
                WINDOW_HEIGHT - 100,
                180,
                50,
            ),
            "Continue",
        )

        self.intro_dialogues = [
            "Welcome to Anya's House!",
            "Anya can read your mind!",
            "Think of any word...",
            "Anya will guess it!",
        ]

        self.dialogue_index = 0

        self.word_length_input = (
            InputField(
                pygame.Rect(
                    WINDOW_WIDTH // 2 - 100,
                    WINDOW_HEIGHT // 2 + 40,
                    200,
                    70,
                ),
                placeholder="0",
            )
        )

        self.word_continue_button = (
            Button(
                pygame.Rect(
                    WINDOW_WIDTH // 2 - 90,
                    WINDOW_HEIGHT // 2 + 140,
                    180,
                    55,
                ),
                "Continue",
            )
        )
        self.matrix_grid = MatrixGrid(
        x=360,
        y=260,
    )

        self.current_letter = 1
        self.revealed_word = ""

        self.play_again_button = Button(
            pygame.Rect(
                WINDOW_WIDTH // 2 - 210,
                WINDOW_HEIGHT - 130,
                180,
                55,
            ),
            "Play Again",
        )

        self.quit_button = Button(
            pygame.Rect(
                WINDOW_WIDTH // 2 + 30,
                WINDOW_HEIGHT - 130,
                180,
                55,
            ),
            "Quit",
        )

        self.transpose_intro_timer = 0


    def load_background(self) -> pygame.Surface:
        image = pygame.image.load(
            SPRITES_DIR / "bg.jpg"
        ).convert()

        return pygame.transform.scale(
            image,
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

    def load_anya_sprites(
        self,
    ) -> list[pygame.Surface]:
        sprites = []

        valid_extensions = (
            ".png",
            ".jpg",
            ".jpeg",
        )

        files = sorted(
            [
                file
                for file in ANYA_DIR.iterdir()
                if file.suffix.lower()
                in valid_extensions
            ]
        )

        for file in files:
            sprite = pygame.image.load(
                file
            ).convert_alpha()

            sprite = pygame.transform.scale(
                sprite,
                (360, 300),
            )

            sprites.append(sprite)

        return sprites

    def run(self) -> None:
        self.audio.play_background_music()

        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if (
                self.state
                == GameState.INTRO
            ):

                if (
                    event.type
                    == pygame.MOUSEBUTTONDOWN
                ):

                    if not (
                        self.dialogue_box
                        .finished_typing
                    ):
                        self.dialogue_box.skip_typing()

                    elif (
                        self.continue_button
                        .is_clicked(event)
                    ):
                        self.advance_intro()

            if (
                event.type
                == pygame.KEYDOWN
            ):
                if (
                    event.key
                    == pygame.K_RETURN
                ):
                    if not (
                        self.dialogue_box
                        .finished_typing
                    ):
                        self.dialogue_box.skip_typing()
            if (
                self.state
                == GameState.WORD_LENGTH
            ):

                self.word_length_input.handle_event(
                    event
                )

                if (
                    event.type
                    == pygame.KEYDOWN
                ):
                    if (
                        event.key
                        == pygame.K_RETURN
                    ):
                        self.submit_word_length()

                if (
                    self.word_continue_button
                    .is_clicked(event)
                ):
                    self.submit_word_length()
            if (
                self.state
                == GameState.MATRIX_SELECTION
            ):

                if (
                    event.type
                    == pygame.KEYDOWN
                ):
                    if (
                        event.unicode.isdigit()
                    ):
                        number = int(
                            event.unicode
                        )

                        if 1 <= number <= 6:
                            self.select_matrix_column(
                                number
                            )

                if (
                    event.type
                    == pygame.MOUSEBUTTONDOWN
                ):

                    column = (
                        self.matrix_grid
                        .get_clicked_column(
                            pygame.mouse.get_pos()
                        )
                    )

                    if column:
                        self.select_matrix_column(
                            column
                        )
            if (
                self.state
                == GameState.TRANSPOSE_SELECTION
            ):

                if (
                    event.type
                    == pygame.KEYDOWN
                ):
                    if (
                        event.unicode.isdigit()
                    ):
                        number = int(
                            event.unicode
                        )

                        if 1 <= number <= 6:
                            self.select_transpose_column(
                                number
                            )

                if (
                    event.type
                    == pygame.MOUSEBUTTONDOWN
                ):

                    column = (
                        self.matrix_grid
                        .get_clicked_column(
                            pygame.mouse.get_pos()
                        )
                    )

                    if column:
                        self.select_transpose_column(
                            column
                        )
            if (
                self.state
                == GameState.REVEAL
            ):

                if (
                    self.play_again_button
                    .is_clicked(event)
                ):
                    self.reset_game()

                elif (
                    self.quit_button
                    .is_clicked(event)
                ):
                    self.running = False
    def update(
        self,
        dt: float,
    ) -> None:

        mouse_pos = (
            pygame.mouse.get_pos()
        )

        self.continue_button.update(
            mouse_pos
        )

        self.dialogue_box.update(dt)

        if (
            self.state
            == GameState.SPLASH
        ):
            self.fade.update(dt)

            if self.fade.finished:
                self.state = (
                    GameState.INTRO
                )

                self.audio.play_dialogue(
                    "welcome"
                )

                self.dialogue_box.set_text(
                    self.intro_dialogues[
                        0
                    ]
                )
        if (
            self.state
            == GameState.WORD_LENGTH
        ):
            self.word_continue_button.update(
                mouse_pos
            )
        if (
            self.state
            == GameState.REVEAL
        ):
            self.play_again_button.update(
                mouse_pos
            )

            self.quit_button.update(
                mouse_pos
            )

        if (
            self.state
            == GameState.TRANSPOSE_INTRO
        ):
            self.transpose_intro_timer += dt

            if (
                self.transpose_intro_timer
                >= 2.5
            ):
                self.state = (
                    GameState
                    .TRANSPOSE_SELECTION
                )
    
    def advance_intro(self) -> None:
        self.dialogue_index += 1

        if (
            self.dialogue_index
            >= len(
                self.intro_dialogues
            )
        ):
            self.state = (
                GameState
                .WORD_LENGTH
            )

            return

        self.dialogue_box.set_text(
            self.intro_dialogues[
                self.dialogue_index
            ]
        )
    def submit_word_length(
        self,
    ) -> None:

        value = (
            self.word_length_input
            .get_value()
        )

        if (
            value is None
            or value <= 0
            or value > 20
        ):
            return

        self.guesser.word_length = (
            value
        )

        self.state = (
            GameState
            .MATRIX_SELECTION
        )
    
    def select_matrix_column(
        self,
        column: int,
    ) -> None:

        self.guesser.selected_columns.append(
            column
        )

        self.current_letter += 1

        if (
            len(
                self.guesser
                .selected_columns
            )
            >= self.guesser.word_length
        ):
            self.state = (
                GameState
                .TRANSPOSE_INTRO
            )

            self.current_letter = 1

            self.transpose_intro_timer = 0

            self.audio.play_dialogue(
                "waku"
            )
    def select_transpose_column(
        self,
        column: int,
    ) -> None:

        self.guesser.transpose_columns.append(
            column
        )

        self.current_letter += 1

        if (
            len(
                self.guesser
                .transpose_columns
            )
            >= self.guesser.word_length
        ):

            self.revealed_word = (
                self.guesser
                .calculate_word()
            )

            self.audio.play_dialogue(
                "gwah"
            )

            self.current_sprite = 2

            self.state = (
                GameState.REVEAL
            )
            pygame.event.clear()
    def render(self) -> None:
        self.screen.blit(
            self.background,
            (0, 0),
        )

        self.render_anya()

        if self.state == GameState.SPLASH:
            self.render_splash()

        elif self.state == GameState.INTRO:
            self.render_intro()
        elif (
            self.state
            == GameState.WORD_LENGTH
        ):
            self.render_word_length()
        
        elif (
            self.state
            == GameState.MATRIX_SELECTION
        ):
            self.render_matrix_selection()
        elif (
            self.state
            == GameState.TRANSPOSE_INTRO
        ):
            self.render_transpose_intro()

        elif (
            self.state
            == GameState.TRANSPOSE_SELECTION
        ):
            self.render_transpose_selection()

        elif (
            self.state
            == GameState.REVEAL
        ):
            self.render_reveal()

        pygame.display.flip()

    def render_anya(self) -> None:

        sprite = self.anya_sprites[
            self.current_sprite
        ]

        dialogue_states = {
            GameState.SPLASH,
            GameState.INTRO,
        }

        sprite_width = sprite.get_width()
        sprite_height = sprite.get_height()

        bottom_margin = 0
        top_margin = DIALOGUE_HEIGHT

        if self.state in dialogue_states:
            x = 260

            y = (
                WINDOW_HEIGHT
                - sprite_height
                - top_margin
            )

        else:
            x = 0 #(WINDOW_WIDTH - sprite_width) for right side...

            y = (
                WINDOW_HEIGHT
                - sprite_height
                - bottom_margin
            )

        sprite_copy = sprite.copy()

        sprite_copy.set_alpha(
            int(self.fade.alpha)
        )

        self.screen.blit(
            sprite_copy,
            (x, y),
        )
    def render_splash(self) -> None:

        self.draw_title_panel()

        self.draw_text(
            "AnyaPath Remastered",
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                145,
            ),
        )

    def render_intro(self) -> None:
        self.dialogue_box.draw(
            self.screen
        )

        if (
            self.dialogue_box
            .finished_typing
        ):
            self.continue_button.draw(
                self.screen
            )
    def render_word_length(
        self,
    ) -> None:

        self.draw_title_panel()

        subtitle_font = pygame.font.Font(
            None,
            42,
        )

        self.draw_text(
            "Think of a word",
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                120,
            ),
        )

        self.draw_text(
            "How many letters does it have?",
            subtitle_font,
            (235, 235, 235),
            (
                WINDOW_WIDTH // 2,
                170,
            ),
        )

        self.word_length_input.draw(
            self.screen
        )

        self.word_continue_button.draw(
            self.screen
        )
    def render_matrix_selection(
        self,
    ) -> None:

        self.draw_title_panel()

        subtitle_font = pygame.font.Font(
            None,
            40,
        )

        self.draw_text(
            (
                f"Letter "
                f"{self.current_letter}"
                f" / "
                f"{self.guesser.word_length}"
            ),
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                120,
            ),
        )

        self.draw_text(
            "Which column contains your letter?",
            subtitle_font,
            (235, 235, 235),
            (
                WINDOW_WIDTH // 2,
                170,
            ),
        )

        self.matrix_grid.draw(
            self.screen,
            self.guesser.MATRIX,
        )
    def render_transpose_intro(
        self,
    ) -> None:

        self.draw_title_panel()

        subtitle_font = pygame.font.Font(
            None,
            42,
        )

        self.draw_text(
            "One more time!",
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                120,
            ),
        )

        self.draw_text(
            "Anya is almost there...",
            subtitle_font,
            (235, 235, 235),
            (
                WINDOW_WIDTH // 2,
                170,
            ),
        )
    def render_transpose_selection(
        self,
    ) -> None:

        self.draw_title_panel()

        subtitle_font = pygame.font.Font(
            None,
            40,
        )

        self.draw_text(
            (
                f"Letter "
                f"{self.current_letter}"
                f" / "
                f"{self.guesser.word_length}"
            ),
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                120,
            ),
        )

        self.draw_text(
            "Which column contains your letter?",
            subtitle_font,
            (235, 235, 235),
            (
                WINDOW_WIDTH // 2,
                170,
            ),
        )

        self.matrix_grid.draw(
            self.screen,
            self.guesser.TRANSPOSED_MATRIX,
        )
    def render_reveal(
        self,
    ) -> None:

        self.draw_title_panel()

        result_font = pygame.font.Font(
            None,
            80,
        )

        self.draw_text(
            "Anya thinks...",
            self.title_font,
            (255, 230, 240),
            (
                WINDOW_WIDTH // 2,
                120,
            ),
        )

        self.draw_text(
            f'"{self.revealed_word}"',
            result_font,
            (255, 255, 255),
            (
                WINDOW_WIDTH // 2,
                280,
            ),
        )

        self.play_again_button.draw(
            self.screen
        )

        self.quit_button.draw(
            self.screen
        )
    def reset_game(self) -> None:

        self.guesser.reset()

        self.current_letter = 1
        self.revealed_word = ""

        self.word_length_input.clear()

        self.current_sprite = 0

        self.state = (
            GameState.WORD_LENGTH
        )

    def draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int],
        shadow: bool = True,
    ) -> None:

        if shadow:
            shadow_surface = font.render(
                text,
                True,
                (20, 20, 20),
            )

            shadow_rect = (
                shadow_surface.get_rect(
                    center=(
                        center[0] + 3,
                        center[1] + 3,
                    )
                )
            )

            self.screen.blit(
                shadow_surface,
                shadow_rect,
            )

        text_surface = font.render(
            text,
            True,
            color,
        )

        text_rect = (
            text_surface.get_rect(
                center=center
            )
        )

        self.screen.blit(
            text_surface,
            text_rect,
        )

    def draw_title_panel(
        self,
    ) -> None:

        panel_width = 720
        panel_height = 120

        panel = pygame.Surface(
            (
                panel_width,
                panel_height,
            ),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            panel,
            (15, 15, 25, 190),
            (
                0,
                0,
                panel_width,
                panel_height,
            ),
            border_radius=24,
        )

        rect = panel.get_rect(
            center=(
                WINDOW_WIDTH // 2,
                150,
            )
        )

        self.screen.blit(
            panel,
            rect,
        )

        pygame.draw.rect(
            self.screen,
            (255, 190, 210),
            rect,
            width=3,
            border_radius=24,
        )