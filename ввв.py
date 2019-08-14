
from livewires import games, color
import math
import random


games.init(screen_width=1200, screen_height=700, fps=50)


class Borehole(games.Sprite):
    """ Скважина. """
    image1 = games.load_image("Images\Borehole1.bmp")
    image2 = games.load_image("Images\Borehole2.bmp")
    coord = [[61, 165], [61, 245], [61, 328], [61, 408], [61, 489], [61, 565], [61, 641],
             [337, 165], [337, 245], [337, 328], [337, 408], [337, 489], [337, 565], [337, 641],
             [411, 165], [411, 245], [411, 328], [411, 408], [411, 489], [411, 565], [411, 641],
             [487, 165], [487, 245], [487, 328], [487, 408], [487, 489], [487, 565], [487, 641],
             [137, 165], [137, 232], [137, 300], [137, 365], [137, 441], [137, 508], [137, 576], [137, 641],
             [261, 165], [261, 232], [261, 300], [261, 365], [261, 441], [261, 508], [261, 576], [261, 641],
             [198, 365], [198, 441],
             [661, 241], [661, 321], [661, 399], [661, 479], [661, 558], [661, 641],
             [737, 241], [737, 321], [737, 399], [737, 479], [737, 558], [737, 641],
             [561, 241], [561, 165],
             [837, 241], [837, 165],
             [629, 165], [698, 165], [766, 165],
             [911, 165], [911, 241], [911, 365], [911, 441], [911, 565], [911, 641], [911, 304],
             [986, 165], [986, 241], [986, 365], [986, 441], [986, 565], [986, 641], [986, 304],
             [1062, 165], [1062, 241], [1062, 365], [1062, 441], [1062, 565], [1062, 641], [1062, 503],
             [1138, 165], [1138, 241], [1138, 365], [1138, 441], [1138, 565], [1138, 641], [1138, 503]]

    mutable_coord = coord[:]
    new_coord = None

    def __init__(self, game):
        """ Инициализирует спрайт с изображением скважины. """
        self.game = game

        self.new_coord = random.choice(self.mutable_coord)
        if len(self.mutable_coord) != 0:
            self.mutable_coord.remove(self.new_coord)

        super(Borehole, self).__init__(image=Borehole.image1,
                                       x=self.new_coord[0],
                                       y=self.new_coord[1],
                                       is_collideable=True)

    def drilling(self):
        super(Borehole, self).__init__(image=Borehole.image2,
                                       x=self.x,
                                       y=self.y,
                                       is_collideable=False)  # ставить ФОЛС чтобы нельзя было взаимодействовать
        self.game.new_borehole()
        self.game.die()
        self.game.advance()


class Drill(games.Sprite):
    """ Бур. """
    image = games.load_image("Images\Drill.bmp")

    def __init__(self, game, x, y, ang, follower):
        """ Инициализирует спрайт с изображением бура. """
        self.game = game
        self.follower = follower
        super(Drill, self).__init__(image=Drill.image,
                                    x=x,
                                    y=y,
                                    angle=ang)

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Borehole):
                    sprite.drilling()

        self.angle = self.follower.angle
        angle = self.angle * math.pi / 180  # преобразование в радианы
        self.x = (self.follower.x - 1) - (38 * -math.sin(angle))
        self.y = self.follower.y - (38 * math.cos(angle))


class Driller(games.Sprite):
    """ Буровая установка. """
    image = games.load_image("Images\Driller.bmp")
    ROTATION_STEP = .5
    VALIOCITY_STEP = .5

    def __init__(self, game, x, y, ang):
        """ Инициализирует спрайт с изображением буровой установки. """
        self.game = game
        super(Driller, self).__init__(image=Driller.image,
                                      x=x,
                                      y=y,
                                      angle=ang)

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        if self.bottom > games.screen.height - 30:
            self.bottom = games.screen.height - 30
        if self.top < 130:
            self.top = 130
        if self.right > games.screen.width - 30:
            self.right = games.screen.width - 30
        if self.left < 30:
            self.left = 30
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Driller.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Driller.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180  # преобразование в радианы
            self.x += Driller.VALIOCITY_STEP * math.sin(angle)
            self.y += Driller.VALIOCITY_STEP * -math.cos(angle)
        if games.keyboard.is_pressed(games.K_DOWN):
            angle = self.angle * math.pi / 180  # преобразование в радианы
            self.x += Driller.VALIOCITY_STEP * -math.sin(angle)
            self.y += Driller.VALIOCITY_STEP * math.cos(angle)


class Game(object):
    """ Собственно игра. """
    drillbg = games.load_image("Images\main2.jpg")
    drill = None
    driller = None
    new_borehole = None
    x_driller = games.screen.width / 2
    y_driller = games.screen.height / 2
    ang_driller = 0
    x_drill = games.screen.width / 2
    y_drill = (games.screen.height / 2) + 50
    ang_drill = 0

    def advance(self):
        """ Создаем скважины и дома. """
        self.driller = Driller(game=self,
                               x=self.x_driller,
                               y=self.y_driller,
                               ang=self.ang_driller)
        games.screen.add(self.driller)

        self.drill = Drill(game=self,
                           x=self.x_drill,
                           y=self.y_drill,
                           ang=self.ang_drill,
                           follower=self.driller)
        games.screen.add(self.drill)

    def die(self):
        self.x_driller = self.driller.x
        self.y_driller = self.driller.y
        self.ang_driller = self.driller.angle
        self.x_drill = self.drill.x
        self.y_drill = self.drill.y
        self.ang_drill = self.drill.angle

        self.driller.destroy()
        self.drill.destroy()

    def new_borehole(self):
        new_borehole = Borehole(game=self)
        games.screen.add(new_borehole)

    def play(self):
        """ Начинает игру. """
        # рисуем фоновую картинку
        games.screen.background = self.drillbg
        # создание скважин
        self.new_borehole()
        # создание буровой машины
        self.advance()
        # начало игры
        games.screen.mainloop()


def main():
    drill_simulator = Game()
    drill_simulator.play()


if __name__ == '__main__':
    main()
