from __future__ import annotations

import pygame

from constants import (
    BLACK,
    BUTTON_FONT_SIZE,
    BUTTON_HOVER,
    BUTTON_IDLE,
    DIALOGUE_BG,
    DIALOGUE_BORDER,
    DIALOGUE_FONT_SIZE,
    DIALOGUE_HEIGHT,
    TEXT_PRIMARY,
    WHITE,
)

class MatrixGrid:
    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:

        self.x = x
        self.y = y

        self.cell_width = 90
        self.cell_height = 52

        self.font = pygame.font.Font(
            None,
            38,
        )

        self.column_rects = []

    def draw(
        self,
        screen: pygame.Surface,
        matrix: list[list[str]],
    ) -> None:

        self.column_rects.clear()

        max_columns = 6

        for col in range(max_columns):

            rect = pygame.Rect(
                self.x + col * self.cell_width,
                self.y - 55,
                self.cell_width - 10,
                50,
            )

            self.column_rects.append(rect)

            hovered = rect.collidepoint(
                pygame.mouse.get_pos()
            )

            color = (
                (255, 210, 230)
                if hovered
                else (255, 180, 210)
            )

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=12,
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                rect,
                width=2,
                border_radius=12,
            )

            number = self.font.render(
                str(col + 1),
                True,
                (20, 20, 20),
            )

            screen.blit(
                number,
                number.get_rect(
                    center=rect.center
                ),
            )

        for row_index, row in enumerate(
            matrix
        ):
            for (
                col_index,
                letter,
            ) in enumerate(row):

                cell_rect = pygame.Rect(
                    self.x
                    + col_index
                    * self.cell_width,
                    self.y
                    + row_index
                    * self.cell_height,
                    self.cell_width - 10,
                    self.cell_height - 8,
                )

                pygame.draw.rect(
                    screen,
                    (35, 35, 45),
                    cell_rect,
                    border_radius=12,
                )

                pygame.draw.rect(
                    screen,
                    (255, 190, 210),
                    cell_rect,
                    width=2,
                    border_radius=12,
                )

                text = self.font.render(
                    letter,
                    True,
                    (255, 255, 255),
                )

                screen.blit(
                    text,
                    text.get_rect(
                        center=cell_rect.center
                    ),
                )

    def get_clicked_column(
        self,
        mouse_pos: tuple[int, int],
    ) -> int | None:

        for (
            index,
            rect,
        ) in enumerate(
            self.column_rects
        ):
            if rect.collidepoint(
                mouse_pos
            ):
                return index + 1

        return None


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
    ) -> None:
        self.rect = rect
        self.text = text

        self.font = pygame.font.Font(
            None,
            BUTTON_FONT_SIZE,
        )

        self.hovered = False

    def update(
        self,
        mouse_pos: tuple[int, int],
    ) -> None:
        self.hovered = self.rect.collidepoint(
            mouse_pos
        )

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        color = (
            BUTTON_HOVER
            if self.hovered
            else BUTTON_IDLE
        )

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=16,
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.rect,
            width=2,
            border_radius=16,
        )

        text_surface = self.font.render(
            self.text,
            True,
            BLACK,
        )

        text_rect = (
            text_surface.get_rect(
                center=self.rect.center
            )
        )

        screen.blit(
            text_surface,
            text_rect,
        )

    def is_clicked(
        self,
        event: pygame.event.Event,
    ) -> bool:
        return (
            event.type
            == pygame.MOUSEBUTTONDOWN
            # and self.hovered
            and self.rect.collidepoint(event.pos)
        )


class DialogueBox:
    def __init__(
        self,
        width: int,
        screen_height: int,
    ) -> None:

        self.rect = pygame.Rect(
            40,
            screen_height
            - DIALOGUE_HEIGHT
            - 30,
            width - 80,
            DIALOGUE_HEIGHT,
        )

        self.font = pygame.font.Font(
            None,
            DIALOGUE_FONT_SIZE,
        )

        self.text = ""
        self.visible_text = ""

        self.char_index = 0

        self.typing_speed = 40
        self.timer = 0

        self.finished_typing = True

    def set_text(
        self,
        text: str,
    ) -> None:
        self.text = text
        self.visible_text = ""

        self.char_index = 0
        self.timer = 0

        self.finished_typing = False

    def skip_typing(self) -> None:
        self.visible_text = self.text
        self.finished_typing = True

    def update(
        self,
        dt: float,
    ) -> None:

        if self.finished_typing:
            return

        self.timer += dt

        interval = (
            1 / self.typing_speed
        )

        while (
            self.timer
            >= interval
            and self.char_index
            < len(self.text)
        ):
            self.timer -= interval

            self.char_index += 1

            self.visible_text = (
                self.text[
                    : self.char_index
                ]
            )

        if (
            self.char_index
            >= len(self.text)
        ):
            self.finished_typing = True

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        pygame.draw.rect(
            screen,
            DIALOGUE_BG,
            self.rect,
            border_radius=22,
        )

        pygame.draw.rect(
            screen,
            DIALOGUE_BORDER,
            self.rect,
            width=3,
            border_radius=22,
        )

        wrapped_lines = (
            self.wrap_text(
                self.visible_text,
                self.rect.width - 40,
            )
        )

        y_offset = self.rect.y + 25

        for line in wrapped_lines:
            text_surface = (
                self.font.render(
                    line,
                    True,
                    TEXT_PRIMARY,
                )
            )

            screen.blit(
                text_surface,
                (
                    self.rect.x + 20,
                    y_offset,
                ),
            )

            y_offset += 38

    def wrap_text(
        self,
        text: str,
        max_width: int,
    ) -> list[str]:

        words = text.split()

        lines = []
        current_line = ""

        for word in words:

            test_line = (
                current_line
                + word
                + " "
            )

            width = self.font.size(
                test_line
            )[0]

            if width <= max_width:
                current_line = (
                    test_line
                )
            else:
                lines.append(
                    current_line
                )

                current_line = (
                    word + " "
                )

        if current_line:
            lines.append(
                current_line
            )

        return lines

class InputField:
    def __init__(
        self,
        rect: pygame.Rect,
        placeholder: str = "",
    ) -> None:

        self.rect = rect
        self.placeholder = placeholder

        self.font = pygame.font.Font(
            None,
            42,
        )

        self.text = ""

        self.active = True

    def handle_event(
        self,
        event: pygame.event.Event,
    ) -> bool:

        if (
            event.type
            != pygame.KEYDOWN
        ):
            return False

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return True

        if (
            event.unicode.isdigit()
            and len(self.text) < 2
        ):
            self.text += (
                event.unicode
            )
            return True

        return False

    def get_value(self) -> int | None:
        if not self.text:
            return None

        return int(self.text)

    def clear(self) -> None:
        self.text = ""

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            border_radius=18,
        )

        pygame.draw.rect(
            screen,
            (255, 190, 210),
            self.rect,
            width=3,
            border_radius=18,
        )

        display_text = (
            self.text
            if self.text
            else self.placeholder
        )

        color = (
            (20, 20, 20)
            if self.text
            else (150, 150, 150)
        )

        text_surface = (
            self.font.render(
                display_text,
                True,
                color,
            )
        )

        text_rect = (
            text_surface.get_rect(
                center=self.rect.center
            )
        )

        screen.blit(
            text_surface,
            text_rect,
        )