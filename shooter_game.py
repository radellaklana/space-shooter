#Create your own shooter

from pygame import *
from random import randint
from time import time as timer


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost_sound = mixer.Sound("lost.wav")
win_sound = mixer.Sound("win.wav")

font.init()
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
lost = 0
score = 0
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, sixe_x, size_y, player_speed, asteroid=False):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_y, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.asteroid = asteroid
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if keys[K_RIGHT]and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost 
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            if self.asteroid == False: 
               lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 900
win_height = 700
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters= sprite.Group()
for i in range(3):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7), True)
    asteroids.add(asteroid)

finish = False
run = True
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e. type == QUIT:
            if e.type == K_SPACE:
        #elif e.type == KEYDOWN:
            #if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >=5 and rel_time == False :
                    last_time = timer()
                    rel_time = True
    if finish != True:
        window.blit(background, (0,0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('wait,reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 
                rel_time =True

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score =score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, True):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            life -= 1
        
        if sprite.spritecollide(ship, asteroids, True):
           asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
           asteroids.add(asteroid)
           life -= 1
 

        if lost >= 3 or life < 1:
            print("lost", lost)
            print("life", life)
            finish = True
            window.blit(lose, (300, 300))
            lost_sound.play()

        if  score >= 10:
            finish = True
            window.blit(win, (300, 300))
            win_sound.play()

        text = font2.render('Score: ' + str(score), 1, (225,225,225))
        window.blit(text, (10,20))

        text_lose = font2.render('Life: ' + str(life), 1, (225,225,225))
        window.blit(text_lose, (10, 50))

        text_lose = font2.render('Lost: ' + str(lost), 1, (225,225,225))
        window.blit(text_lose, (10, 80))

    display.update()
    time.delay(50)
