class FadeAnimation:
    def __init__(
        self,
        speed: float = 250,
    ) -> None:
        self.alpha = 0
        self.speed = speed
        self.finished = False

    def reset(self) -> None:
        self.alpha = 0
        self.finished = False

    def update(self, dt: float) -> None:
        if self.finished:
            return

        self.alpha += self.speed * dt

        if self.alpha >= 255:
            self.alpha = 255
            self.finished = True
