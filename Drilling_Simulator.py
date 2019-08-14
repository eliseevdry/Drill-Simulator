
from livewires import games, color
import math
import random


games.init(screen_width=1200, screen_height=700, fps=50)


class Buffer(games.Sprite):
    """ Уничтожает бытовки. """
    image = games.load_image("Images\Buffer.bmp")

    def __init__(self, game, x, y, follower):
        """ Инициализирует спрайт с изображением бытовки. """
        self.game = game
        self.follower = follower
        super(Buffer, self).__init__(image=Buffer.image,
                                     x=x,
                                     y=y)

    def update(self):
        self.angle = self.follower.angle
        angle = self.angle * math.pi / 180  # преобразование в радианы
        self.x = self.follower.x - (-17 * -math.sin(angle))
        self.y = self.follower.y - (-17 * math.cos(angle))

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Home):
                    sprite.die()


class Home(games.Sprite):
    """ Бытовка. """
    image1 = games.load_image("Images\home.bmp")
    image2 = games.load_image("Images\home_destroy.bmp")

    def __init__(self, game, x, y):
        """ Инициализирует спрайт с изображением бытовки. """
        self.game = game
        super(Home, self).__init__(image=Home.image1,
                                   x=x,
                                   y=y)

    def die(self):
        """ Разрушает объект. """
        super(Home, self).__init__(image=Home.image2,
                                   x=self.x,
                                   y=self.y)


class Borehole(games.Sprite):
    """ Скважина. """
    image1 = games.load_image("Images\Borehole1.bmp")
    image2 = games.load_image("Images\Borehole2.bmp")
    #time = 5160
    #total = 0
    total_sprites = []

    def __init__(self, game, x, y):
        """ Инициализирует спрайт с изображением скважины. """
        #Borehole.total += 1
        #Borehole.time += 860
        self.game = game

        Borehole.total_sprites = game.sprites[:]

        super(Borehole, self).__init__(image=Borehole.image1,
                                       x=x,
                                       y=y,
                                       is_collideable=True)

        self.borehole_new()


        #self.location = games.Text(value="""  {0}   {1}""".format(self.x, self.y), #(665 - self.y, self.x - 35)
                                   #size=30,
                                   #color=color.red,
                                   #top=40,
                                   #left=40,
                                   #is_collideable=False)
        #games.screen.add(self.location)

        #self.text = "{0}".format(math.trunc(Borehole.time / 86))

        #self.sec = games.Text(value=self.text,
                              #size=100,
                              #color=color.white,
                              #top=20,
                              #right=games.screen.width - 40,
                              #is_collideable=False)
        #games.screen.add(self.sec)

    def borehole_new(self):
        pass
        #self.bore = self.total_sprites[0]

    def update(self):
        pass
        #Borehole.time -= 1
        #self.text = "{0}".format(math.trunc(Borehole.time / 86))
        #self.sec.set_value(self.text)
        #if Borehole.time <= 0:
            #self.game.end()

    def drilling(self):
        super(Borehole, self).__init__(image=Borehole.image2,
                                       x=self.x,
                                       y=self.y,
                                       is_collideable=False) # обязательно ставить ФОЛС чтобы нельзя было взаимодействовать


class Drill(games.Sprite):
    """ Бур. """
    image = games.load_image("Images\Drill.bmp")
    #time = 0
    #text = None

    def __init__(self, game, x, y, follower):
        """ Инициализирует спрайт с изображением бура. """
        self.game = game
        self.follower = follower
        super(Drill, self).__init__(image=Drill.image,
                                    x=x,
                                    y=y)

        #self.text = "  {0}   {1}".format(math.trunc(665 - self.y), math.trunc(self.x - 35))

        #self.coord = games.Text(value="X        Y",
                                #size=30,
                                #color=color.red,
                                #top=10,
                                #left=60,
                                #is_collideable=False)

        #self.location = games.Text(value=self.text,
                                   #size=30,
                                   #color=color.blue,
                                   #top=70,
                                   #left=40,
                                   #is_collideable=False)

        #games.screen.add(self.location)
        #games.screen.add(self.coord)

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """
        #self.time += 1

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Borehole):
                    #self.follower.freeze()
                    sprite.drilling()

        #if self.time == 50:
            #self.text = "  {0}   {1}".format(math.trunc(665 - self.y), math.trunc(self.x - 35))
            #self.location.set_value(self.text)
            #self.time = 0

        self.angle = self.follower.angle
        angle = self.angle * math.pi / 180  # преобразование в радианы
        self.x = (self.follower.x - 1) - (38 * -math.sin(angle))
        self.y = self.follower.y - (38 * math.cos(angle))


class Driller(games.Sprite):
    """ Буровая установка. """
    image = games.load_image("Images\Driller.bmp")
    ROTATION_STEP = .5
    VALIOCITY_STEP = .5
    VALIOCITY_MAX = 3

    #freeze_time = 0

    def __init__(self, game, x, y):
        """ Инициализирует спрайт с изображением космического корабля. """
        self.game = game
        super(Driller, self).__init__(image=Driller.image,
                                      x=x,
                                      y=y)

        #self.text = "  {0}  ".format(self.freeze_time)
        #self.frost = games.Text(value=self.text,
                                #size=60,
                                #color=color.red,
                                #top=40,
                                #left=500,
                                #is_collideable=False)
        #games.screen.add(self.frost)

    def freeze(self):
        pass
        #if self.freeze_time == 0:
            #self.freeze_time = 500

    def update(self):
        """ Переносит спрайт на противоположную сторону окна. """

        #self.text = "  {0}  ".format(self.freeze_time)
        #self.frost.set_value(self.text)

        if self.bottom > games.screen.height - 30:
            self.bottom = games.screen.height - 30
        if self.top < 130:
            self.top = 130
        if self.right > games.screen.width - 30:
            self.right = games.screen.width - 30
        if self.left < 30:
            self.left = 30

        #if self.freeze_time <= 0:
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
        #if self.freeze_time > 0:
            #self.freeze_time -= 1
            #if games.keyboard.is_pressed(games.K_LEFT):
                #self.angle -= 0
            #if games.keyboard.is_pressed(games.K_RIGHT):
                #self.angle += 0
            #if games.keyboard.is_pressed(games.K_UP):
                #self.x += 0
                #self.y += 0
            #if games.keyboard.is_pressed(games.K_DOWN):
                #self.x += 0
                #self.y += 0


class Game(object):
    """ Собственно игра. """
    sprites = []
    total_sprites = []
    total_random = []

    def __init__(self):
        """ Инициализирует объект Game. """
        pass

    def advance(self):
        """ Создаем скважины и дома. """

        self.coord_h = [[178, 291], [178, 312], [178, 333], [178, 643],
                        [216, 471], [216, 492], [216, 513], [216, 534], [216, 555],
                        [612, 271], [612, 292], [612, 313], [612, 334], [612, 595], [612, 616], [612, 637],
                        [903, 482], [903, 503], [903, 524],
                        [955, 482], [955, 503], [955, 524],
                        [1006, 482], [1006, 503], [1006, 524],
                        [1035, 275], [1035, 296],
                        [1087, 275]]

        for i in range(len(self.coord_h)):
            home = Home(game=self, x=self.coord_h[i][0], y=self.coord_h[i][1])
            games.screen.add(home)

        driller = Driller(game=self,
                          x=games.screen.width / 2,
                          y=games.screen.height / 2)

        games.screen.add(driller)

        buffer = Buffer(game=self,
                        x=games.screen.width / 2,
                        y=games.screen.height / 2,
                        follower=driller)

        games.screen.add(buffer)

        drill = Drill(game=self,
                      x=games.screen.width / 2,
                      y=(games.screen.height / 2) + 50,
                      follower=driller)

        games.screen.add(drill)

    def end(self):
        """ Завершает игру. """
        # 5-секундное отображение 'Game Over'
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width/2,
                                    y=games.screen.width/3,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)

    def play(self):
        """ Начинает игру. """
        # загрузка и назначение фоновой картинки
        drillbg = games.load_image("Images\main2.jpg")
        games.screen.background = drillbg

        self.coord = [[61, 165], [61, 245], [61, 328], [61, 408], [61, 489], [61, 565], [61, 641],
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

        for i in range(len(self.coord)):
            borehole = Borehole(game=self, x=self.coord[i][0], y=self.coord[i][1])
            self.sprites.append(borehole)
            games.screen.add(borehole)

        self.sprites = self.sprites

        print(self.sprites)

        # создание скважин
        self.advance()
        # начало игры
        games.screen.mainloop()


def main():
    drill_simulator = Game()
    drill_simulator.play()


if __name__ == '__main__':
    main()
