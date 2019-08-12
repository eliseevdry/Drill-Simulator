
from livewires import games, color
import math


games.init(screen_width=1200, screen_height=700, fps=50)


class Home(games.Sprite):
    """ Бытовка. """
    image1 = games.load_image("Images\home.bmp")
    image2 = games.load_image("Images\home_destroy.bmp")

    def __init__(self):
        """ Инициализирует спрайт с изображением бытовки. """
        super(Home, self).__init__(image=Home.image1,
                                   x=1000,
                                   y=500)

    def die(self):
        """ Разрушает объект. """
        super(Home, self).__init__(image=Home.image2,
                                   x=1000,
                                   y=500)



class Borehole(games.Sprite):
    """ Скважина. """
    image1 = games.load_image("Images\Borehole1.bmp")
    image2 = games.load_image("Images\Borehole2.bmp")
    time = 5160

    def __init__(self):
        """ Инициализирует спрайт с изображением скважины. """
        super(Borehole, self).__init__(image=Borehole.image1,
                                       x=1116,
                                       y=168)

        self.location = games.Text(value="""  {0}   {1}""".format(665 - self.y, self.x - 35),
                                   size=30,
                                   color=color.red,
                                   top=40,
                                   left=40,
                                   is_collideable=False)
        games.screen.add(self.location)

        self.text = "{0}".format(math.trunc(self.time / 86))

        self.sec = games.Text(value=self.text,
                              size=100,
                              color=color.white,
                              top=20,
                              right=games.screen.width - 40,
                              is_collideable=False)
        games.screen.add(self.sec)

    def update(self):
        self.time -= 1
        self.text = "{0}".format(math.trunc(self.time / 86))
        self.sec.set_value(self.text)
        if self.time <= 0:
            self.time = 5160

    def drilling(self):
        super(Borehole, self).__init__(image=Borehole.image2,
                                       x=self.x,
                                       y=self.y,
                                       is_collideable=False) # обязательно ставить ФОЛС чтобы нельзя было взаимодействовать



class Drill(games.Sprite):
    """ Бур. """
    image = games.load_image("Images\Drill.bmp")
    time = 0
    text = None

    def __init__(self):
        """ Инициализирует спрайт с изображением бура. """
        super(Drill, self).__init__(image=Drill.image,
                                    x=games.screen.width / 2,
                                    y=(games.screen.height / 2) + 50)

        self.text = "  {0}   {1}".format(math.trunc(665 - self.y), math.trunc(self.x - 35))

        self.coord = games.Text(value="X        Y",
                                size=30,
                                color=color.red,
                                top=10,
                                left=60,
                                is_collideable=False)

        self.location = games.Text(value=self.text,
                                   size=30,
                                   color=color.blue,
                                   top=70,
                                   left=40,
                                   is_collideable=False)

        games.screen.add(self.location)
        games.screen.add(self.coord)

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        self.time += 1

        if self.time == 50:
            self.text = "  {0}   {1}".format(math.trunc(665 - self.y), math.trunc(self.x - 35))
            self.location.set_value(self.text)
            self.time = 0

        self.angle = driller.angle
        angle = self.angle * math.pi / 180  # преобразование в радианы
        self.x = (driller.x - 1) - (38 * -math.sin(angle))
        self.y = driller.y - (38 * math.cos(angle))

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Home):
                    sprite.die()
                if isinstance(sprite, Borehole):
                    driller.freeze()
                    sprite.drilling()


class Driller(games.Sprite):
    """ Буровая установка. """
    image = games.load_image("Images\Driller.bmp")
    ROTATION_STEP = .5
    VALIOCITY_STEP = .5
    VALIOCITY_MAX = 3

    freeze_time = 0

    def __init__(self):
        """ Инициализирует спрайт с изображением космического корабля. """
        super(Driller, self).__init__(image=Driller.image,
                                      x=games.screen.width / 2,
                                      y=(games.screen.height / 2) + 50)

        self.text = "  {0}  ".format(self.freeze_time)
        self.frost = games.Text(value=self.text,
                                size=60,
                                color=color.red,
                                top=40,
                                left=500,
                                is_collideable=False)
        games.screen.add(self.frost)

    def freeze(self):
        if self.freeze_time == 0:
            self.freeze_time = 500

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """

        self.text = "  {0}  ".format(self.freeze_time)
        self.frost.set_value(self.text)

        if self.bottom > games.screen.height - 30:
            self.bottom = games.screen.height - 30
        if self.top < 130:
            self.top = 130
        if self.right > games.screen.width - 30:
            self.right = games.screen.width - 30
        if self.left < 30:
            self.left = 30

        if self.freeze_time <= 0:
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
        if self.freeze_time > 0:
            self.freeze_time -= 1
            if games.keyboard.is_pressed(games.K_LEFT):
                self.angle -= 0
            if games.keyboard.is_pressed(games.K_RIGHT):
                self.angle += 0
            if games.keyboard.is_pressed(games.K_UP):
                self.x += 0
                self.y += 0
            if games.keyboard.is_pressed(games.K_DOWN):
                self.x += 0
                self.y += 0


bg_drill = games.load_image("Images\main2.jpg")


games.screen.background = bg_drill


driller = Driller()
drill = Drill()
home = Home()
borehole = Borehole()
games.screen.add(home)
games.screen.add(borehole)
games.screen.add(driller)
games.screen.add(drill)

games.screen.mainloop()


if __name__ == '__main__':
    main()
