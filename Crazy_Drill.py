
from livewires import games, color
import math
import random


games.init(screen_width=1200, screen_height=700, fps=50)


class Plus(games.Animation):
    """ Анимация прибавления секунд. """
    images = ["Images\plus\P0.bmp",
              "Images\plus\P1.bmp",
              "Images\plus\P2.bmp",
              "Images\plus\P3.bmp",
              "Images\plus\P4.bmp",
              "Images\plus\P5.bmp"]

    def __init__(self):
        super(Plus, self).__init__(images=Plus.images,
                                   x=1083, y=102,
                                   repeat_interval=10, n_repeats=1,
                                   is_collideable=False)


class Loading(games.Animation):
    """ Анимация загрузки. """
    images = ["Images\loading\L0.bmp",
              "Images\loading\L1.bmp",
              "Images\loading\L2.bmp",
              "Images\loading\L3.bmp",
              "Images\loading\L4.bmp",
              "Images\loading\L5.bmp",
              "Images\loading\L6.bmp",
              "Images\loading\L7.bmp",
              "Images\loading\L8.bmp",
              "Images\loading\L9.bmp",
              "Images\loading\L10.bmp"]

    def __init__(self):
        super(Loading, self).__init__(images=Loading.images,
                                      x=600, y=50,
                                      repeat_interval=50, n_repeats=1,
                                      is_collideable=False)


class Borehole(games.Sprite):
    """ Скважина. """
    image1 = games.load_image("Images\Borehole1.bmp")
    image2 = games.load_image("Images\Borehole2.bmp")
    # создаем список координат наших скважин
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

    # создаем копию списка координат, чтобы можно было ее безболезненно изменять
    mutable_coord = coord[:]

    new_coord = None

    def __init__(self, game):
        """ Инициализирует спрайт с изображением скважины. """
        self.game = game

        # выбираем случайные координаты из списка координат скважин
        self.new_coord = random.choice(self.mutable_coord)
        # пока длинна списка координат скважины не станет равна нулю, удаляем из списка выбранные ранее координаты
        if len(self.mutable_coord) != 0:
            self.mutable_coord.remove(self.new_coord)

        # создаем спрайт с новыми случайными координатами
        super(Borehole, self).__init__(image=Borehole.image1,
                                       x=self.new_coord[0],
                                       y=self.new_coord[1],
                                       is_collideable=True)

    def drilling(self):
        # ПРОЦЕСС БУРЕНИЯ
        # меняем изображение скважины и делаем ее пассивной с точки зрения взаимодействия
        super(Borehole, self).__init__(image=Borehole.image2,
                                       x=self.x,
                                       y=self.y,
                                       is_collideable=False)  # ставить ФОЛС чтобы нельзя было взаимодействовать
        # создаем новую скважину в другом месте
        self.game.new_borehole()
        # чтобы вновь созданный спрайт скважины не перекрывал буровую машину нужно сделать его приоритетным
        # для этого сначала удаляем спрайт буровой машины и бура
        self.game.die()
        # и тут же создаем их заново с теми же координатами и углом поворота
        self.game.advance()
        # вызываем метод FROST объекта Game, который на определенное время заморозит нашу буровую машину
        self.game.frost()
        # инициализируем анимацию загрузки
        self.game.loading()



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
        """ Действия бура в реальном времени. """
        # проверяем перекрытие бура со скважиной
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if isinstance(sprite, Borehole):
                    sprite.drilling()
        # задаем физику движения бура в зависимости от движения буровой машины
        self.angle = self.follower.angle
        angle = self.angle * math.pi / 180  # преобразование в радианы
        self.x = (self.follower.x - 1) - (38 * -math.sin(angle))
        self.y = self.follower.y - (38 * math.cos(angle))


class Driller(games.Sprite):
    """ Буровая машина. """
    image = games.load_image("Images\Driller.bmp")
    ROTATION_STEP = .5
    VALIOCITY_STEP = .5
    freeze_time = 0
    # переменная времени
    total_time = 5699
    time_text = None
    minutes = 0
    secounds = 0

    def __init__(self, game, x, y, ang):
        """ Инициализирует спрайт с изображением буровой машины. """
        self.game = game
        super(Driller, self).__init__(image=Driller.image,
                                      x=x,
                                      y=y,
                                      angle=ang)

    def update(self):
        """ Действия буровой машины в реальном времени. """
        Driller.minutes = math.trunc(Driller.total_time / 5160)
        if Driller.minutes > 0:
            Driller.secounds = math.trunc(Driller.total_time / 86) - 60 * Driller.minutes
        else:
            Driller.secounds = math.trunc(Driller.total_time / 86)
        Driller.time_text = "{0}:{1}".format(Driller.minutes, Driller.secounds)
        self.game.sec.set_value(Driller.time_text)
        # создаем рамки движения буровой машины
        if self.bottom > games.screen.height - 30:
            self.bottom = games.screen.height - 30
        if self.top < 130:
            self.top = 130
        if self.right > games.screen.width - 30:
            self.right = games.screen.width - 30
        if self.left < 30:
            self.left = 30
        # описываем физику движения буровой машины
        if self.freeze_time <= 0:
            Driller.total_time -= 1
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
            Driller.total_time -= 0
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

    def freeze(self):
        self.freeze_time = 10 * games.screen.fps
        Driller.total_time += 860


class Game(object):
    """ Собственно игра. """
    drillbg = games.load_image("Images\main2.jpg")
    # инициализаторы спрайтов
    drill = None
    driller = None
    new_borehole = None
    # координаты спрайтов для удаления и создания
    x_driller = games.screen.width / 2
    y_driller = games.screen.height / 2
    ang_driller = 0
    x_drill = games.screen.width / 2
    y_drill = (games.screen.height / 2) + 50
    ang_drill = 0

    def __init__(self):
        self.sec = games.Text(value="1:00",
                              size=100,
                              color=color.white,
                              top=20,
                              right=games.screen.width - 40,
                              is_collideable=False)
        games.screen.add(self.sec)

    def advance(self):
        """ Создаем буровую машину и бур. """
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

    def frost(self):
        self.driller.freeze()

    def loading(self):
        # создание анимации загрузки
        new_loading = Loading()
        games.screen.add(new_loading)
        # создание анимации прибавления секунд
        new_plus = Plus()
        games.screen.add(new_plus)


    def die(self):
        # запоминаем последние координаты и углы спрайтов
        self.x_driller = self.driller.x
        self.y_driller = self.driller.y
        self.ang_driller = self.driller.angle
        self.x_drill = self.drill.x
        self.y_drill = self.drill.y
        self.ang_drill = self.drill.angle
        # удаляем спрайты
        self.driller.destroy()
        self.drill.destroy()

    def new_borehole(self):
        # создаем новую скважину
        new_borehole = Borehole(game=self)
        games.screen.add(new_borehole)

    def play(self):
        """ Начинает игру. """
        # рисуем фоновую картинку
        games.screen.background = self.drillbg
        # создание первой скважины
        self.new_borehole()
        # создание буровой машины и бура
        self.advance()
        # начало игры
        games.screen.mainloop()


def main():
    drill_simulator = Game()
    drill_simulator.play()


if __name__ == '__main__':
    main()
