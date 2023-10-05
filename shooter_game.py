from pygame import *
from random import *
import time as py_time


#создай окно игры
window_size = [700, 500]
#задай фон сцены
window = display.set_mode(window_size)
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), window_size)


#создай 2 спрайта и размести их на сцене
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image,x_size , y_size, x_cor, y_cor, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(x_size, y_size))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()   
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed 
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed 
      
    def fire(self):
        bullet = Bullet('bullet.png', 15,25, player.rect.centerx, player.rect.top, 6)
        bullets.add(bullet)    


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(0,660)
            global lost
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(0,660)

player = Player('rocket.png',65, 65, 300, 430, 10)
   
asteroids = sprite.Group()   
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', 60, 50, randint(0,660), randint(-30, 1), randint(1, 3))
    monsters.add(monster)

for r in range(3):
    asteroid = Asteroid('asteroid.png', 65, 65, randint(0,660), randint(-30, 1), randint(1, 3))
    asteroids.add(asteroid)

font.init()
f = font.SysFont('Arial', 33)
win = f.render('You WIN', True, [215, 215, 0])
lose = f.render('You LOSE', True, [230, 4, 8])

mixer.init()
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
mixer.music.play()

FPS = 60
clock = time.Clock()
lost = 0
kill = 0
game = True
finish = False
newbul = False
bul = 5
timer = 0 
rel = ''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if bul != 0:
                    bul -= 1
                    player.fire()
                    fire.play()
                
    if finish != True:
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list1 = sprite.groupcollide(asteroids, bullets, False, True)
        for collide in sprites_list:
            kill += 1
            monster = Enemy('ufo.png', 65, 65, randint(0,660), randint(-30, 1), randint(1, 2))
            monsters.add(monster)

        if bul <= 0:
            newbul = True 
            rel = 'Перезарядка'
        if newbul:
            if timer == 0:
                timer = py_time.time()
            if py_time.time() - timer >= 3:
                bul = 5
                newbul = False
                timer = 0
                rel = ' '


        window.blit(background, (0,0))
        losts = f.render('Пропущено:' + str(lost), True, [255,255,255])
        kills = f.render('Убито:' + str(kill), True, [255, 255, 255])
        bul_amount = f.render('Пули:' + str(bul), True, [255, 255, 255])
        reloading = f.render(rel, True, [255, 255,255])

        window.blit(bul_amount,(600, 10))
        window.blit(kills,(0,10))
        window.blit(losts,(0,29))
        window.blit(reloading,(240, 410))

        asteroids.draw(window)
        bullets.draw(window)
        monsters.draw(window)
        player.reset()
        
        if kill >= 10:
            window.blit(win,(300, 230))
            finish = True
        if lost >= 3:
            window.blit(lose,(300,230))
            finish = True

        
    display.update()
    clock.tick(FPS)