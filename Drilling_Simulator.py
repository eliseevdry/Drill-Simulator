
from livewires import games, color
import math

games.init(screen_width=1200, screen_height=700, fps=50)

class Driller(games.Sprite):
    """ Буровая установка. """
    image = games.load_image("Images\Driller.bmp")
    ROTATION_STEP = 5
    VALIOCITY_STEP = .03
    VALIOCITY_MAX = 3

    def __init__(self):
        """ Инициализирует спрайт с изображением космического корабля. """
        super(Driller, self).__init__(image=Driller.image,
                                      x=games.screen.width / 2,
                                      y=(games.screen.height / 2) - 100)

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        if self.top > games.screen.height - 50:
            self.bottom = 150
        if self.bottom < 150:
            self.top = games.screen.height - 50
        if self.left > games.screen.width - 50:
            self.right = 50
        if self.right < 50:
            self.left = games.screen.width - 50

        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Driller.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Driller.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180  # преобразование в радианы
            self.dx += Driller.VALIOCITY_STEP * math.sin(angle)
            self.dy += Driller.VALIOCITY_STEP * -math.cos(angle)

# загрузка и назначение фоновой картинки
bg_drill = games.load_image("Images\main2.jpg")
games.screen.background = bg_drill

driller = Driller()
games.screen.add(driller)
games.screen.mainloop()


if __name__ == '__main__':
    main()
