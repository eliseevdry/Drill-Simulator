import pygame

pygame.init()

sc = pygame.display.set_mode((300, 200))
sc.fill((255, 255, 255))

f1 = pygame.font.Font(None, 36)
text1 = f1.render('Hello Привет', 1, (180, 0, 0))

f2 = pygame.font.Font('Fonts/Fixedsys.ttf', 36)
text2 = f2.render("World Мир", 0, (0, 180, 0))

sc.blit(text1, (10, 50))
sc.blit(text2, (10, 100))

pygame.display.update()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()