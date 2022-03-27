from pygame import * 
from random import randint
'''Необходимые классы'''

lost = 0
score = 0
#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0 :
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630 :
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430 :
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)

            if self.speed == 5:
                score -= 1
            elif self.speed == 4:
                score -= 5
            elif self.speed == 3:
                score -= 10
            elif self.speed == 2:
                score -= 15
            else:
                score -= 20


            self.speed = randint(1, 5)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# class Enemy(GameSprite):
#     direction = "left"
#     def updatehorizontal(self, left, right):
#         if self.rect.x <= left:
#             self.direction = "right"
#         if self.rect.x >= right:
#             self.direction = "left"
    
#         if self.direction == "left":
#             self.rect.x -= self.speed
#         else:
#             self.rect.x += self.speed

#     def updatevertical(self, top, bottom):
#         if self.rect.y <= top:
#             self.direction = "bottom"
#         if self.rect.y >= bottom:
#             self.direction = "top"
    
#         if self.direction == "top":
#             self.rect.y -= self.speed
#         else:
#             self.rect.y += self.speed
 
#Персонажи игры:
#player = Player('rocket.png', 70, 380, 4)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#money = mixer.Sound('money.ogg')
scream = mixer.Sound('fire.ogg')

bullets_count = 0

lifes = 10

font.init()
font1 = font.SysFont('Arial', 30)
menutext = font1.render('Нажмите R для продолжения', True, (105, 255, 55))
lose = font1.render('Проигрыш', True, (105, 255, 55))
win = font1.render('Победа', True, (105, 255, 55))
 
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Brawl Stars")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
 
screamer = transform.scale(image.load('scp.jpg'), (win_width, win_height))
menu = transform.scale(image.load('menu.jpg'), (win_width, win_height))


ship = Player('rocket.png', 5, win_width - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(4):
    monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid  = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

fire_sound = mixer.Sound('fire.ogg')
bullets = sprite.Group()

game = True
clock = time.Clock()
FPS = 60


finish =  False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                finish = True
            if e.key == K_r:
                finish = False
            if e.key == K_l:
                score = 0
                lost = 0
                for m in monsters:
                    m.rect.y = -100
            if e.key == K_SPACE and bullets_count < 10:
                fire_sound.play()
                ship.fire()
                bullets_count += 1
                waittime = 0 


    if not finish:
        window.blit(background,(0, 0))
        ship.reset()
        monsters.update()
        monsters.draw(window)
        ship.update()
        asteroids.draw(window)
        asteroids.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(100, 600), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            if sprite.spritecollide(ship, monsters, True):
                monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                monsters.add(monster)
            if sprite.spritecollide(ship, asteroids, True):  
                asteroid  = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                asteroids.add(asteroid)
            #finish = True
            #window.blit(lose, (200, 200))
            lifes -= 1

        if lifes <= 0 or lost > 5:
            finish = True

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        bullets.update()
        bullets.draw(window)

        lifestext = font1.render('Жизней:' + str(lifes), True, (105, 255, 55))
        window.blit(lifestext, (500, 10))
        text_lose = font1.render('Пропущенно: ' + str(lost), 1, (0, 255, 0))
        window.blit(text_lose, (10, 10))
        text_score = font1.render('Счет: ' + str(score), 1, (0, 255, 0))
        window.blit(text_score, (10, 30))

        if ship.rect.y < 0:      
            window.blit(screamer, (0,0))
            scream.play()

        if bullets_count == 10 and waittime < 10:
            text = font1.render('Перезарядка', True, (0, 255, 0))
            window.blit(text, (200, 200))
            waittime += 1
        elif bullets_count == 10 and waittime >= 10:
            waittime = 0
            bullets_count = 0

    else:
        window.blit(menu, (0,0))
        window.blit(menutext, (100, 100))
        score = 0
        lost = 0
        lifes = 10
        for m in monsters:
            m.rect.y = -100
        for a in asteroids:
            a.rect.y = -100



    display.update()
    clock.tick(FPS)