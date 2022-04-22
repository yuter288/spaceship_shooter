#Создай собственный Шутер!
from random import *
from pygame import *
import time as tm
mixer.init()
font.init()
font1 = font.SysFont('Arial', 36)
run=True
wait_f_t=False
monsters = sprite.Group()
asteroids = sprite.Group()
meds = sprite.Group()
num_fire = 0
bullets = sprite.Group()
clock = time.Clock()
FPS = 60
global not_lost
global med
health = 3
num_fire=0
time_now=False
not_lost = 0
finish=False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_weight, palyer_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_weight, palyer_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx,self.rect.top, 15, 10, 20)
        bullets.add(bullet)
        fire_sound.play()
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,550)
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class med_kit(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,550)
            if med > 0:    
                med = med - 1
            
#создание объектов 
win_width = 700
win_height = 500
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))
player=Player('rocket.png', 285, 400, 10, 60, 65)
for i in range (5):
    monster=Enemy('ufo.png', randint(0,600), 0, randint(2,4), 85, 65)
    monsters.add(monster)
for i in range (1):
    med_e =Enemy('first-aid.png',randint(0,550), 0, 2, 85, 65)
    meds.add(med_e)
for i in range (2):
    asteroid=Enemy('asteroid.png', randint(0,600), 0 ,1 , 85, 65)
    asteroids.add(asteroid)

#создание музыкиa
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.2)
fire_sound.set_volume(0.1)
#игровой цикл
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if time_now == False:
                    if num_fire <= 8:   
                        player.fire()
                        num_fire=num_fire+1
                    else:
                        curn_time=tm.time()
                        time_now=True
                else:
                    if tm.time()-curn_time>=3:
                        time_now = False
                        num_fire=0
                        wait_f_t = False
                    else:
                        wait_f_t = True
    if finish !=True:
        window.blit(background,(0,0))
        if wait_f_t==True:
            text_wait = font1.render('ПЕРЕЗАРЯЖАЮСЬ' + str('....'), 1, (255,0,0))
            window.blit(text_wait, (275,250))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        meds.draw(window)
        meds.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,55,255))
        text_score = font1.render('Счёт:' + str(not_lost), 0, (255,55,255))
        text_life = font1.render('Жизни: ' + str(health), 0, (255,0,0))
        window.blit(text_lose, (0,0))
        window.blit(text_score, (0,50))
        window.blit(text_life, (580,0))
        sprite_list2 = sprite.groupcollide(meds, bullets, True, True)
        for i in sprite_list2:
            health=health+1
            med_e =Enemy('first-aid.png',randint(0,550), 0, 1, 85, 65)
            meds.add(med_e)
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            not_lost=not_lost+1
            monster=Enemy('ufo.png', randint(0,600), 0, randint(2,4), 85, 65)
            monsters.add(monster)
        sprite_list3 = sprite.spritecollide(player, asteroids, True)
        for i in sprite_list3:
            health=health-1
            asteroid=Enemy('asteroid.png', randint(0,600), 0 ,1 , 85, 65)
            asteroids.add(asteroid)
        if lost > 100:
            finish = True
            fon_fon=GameSprite('fon.png',0,0,0,700,500)
            fon_fon.reset()
            text_not_win = font1.render('Ты не успел сбить всех', 1, (255,0,0))
            window.blit(text_not_win, (275,250))
            mixer.music.set_volume(0)
            fire_sound.set_volume(0)
        if health<=0:
            finish = True
            fon_fon=GameSprite('fon.png',0,0,0,700,500)
            fon_fon.reset()
            text_not_win = font1.render('Тебя сбил астэроид', 1, (255,0,0))
            window.blit(text_not_win, (275,250))
            mixer.music.set_volume(0)
            fire_sound.set_volume(0)
        if not_lost > 100:
            finish = True
            fon_fon=GameSprite('fon.png',0,0,0,700,500)
            fon_fon.reset()
            text_win = font1.render('Поздравляю, ты успел сбить всех', 1, (0,255,0))
            window.blit(text_win, (275,250))
            mixer.music.set_volume(0)
            fire_sound.set_volume(0)
    display.update()
    clock.tick(FPS)


