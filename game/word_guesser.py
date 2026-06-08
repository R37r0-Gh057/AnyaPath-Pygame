from dataclasses import dataclass, field


@dataclass
class WordGuesser:
    word_length: int = 0
    selected_columns: list[int] = field(default_factory=list)
    transpose_columns: list[int] = field(default_factory=list)

    MATRIX = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V", "W", "X"],
        ["Y", "Z"],
    ]

    TRANSPOSED_MATRIX = [
        ["A", "G", "M", "S", "Y"],
        ["B", "H", "N", "T", "Z"],
        ["C", "I", "O", "U"],
        ["D", "J", "P", "V"],
        ["E", "K", "Q", "W"],
        ["F", "L", "R", "X"],
    ]

    def reset(self) -> None:
        self.word_length = 0
        self.selected_columns.clear()
        self.transpose_columns.clear()

    def calculate_word(self) -> str:
        """Calculate guessed word based on selections."""

        if (
            len(self.selected_columns) != self.word_length
            or len(self.transpose_columns) != self.word_length
        ):
            raise ValueError("Incomplete selection data.")

        letters = []

        for row, column in zip(
            self.transpose_columns,
            self.selected_columns
        ):
            try:
                letter = self.MATRIX[row - 1][column - 1]
                letters.append(letter)
            except IndexError:
                raise ValueError(
                    f"Invalid matrix position ({row}, {column})"
                )

        return "".join(letters)
