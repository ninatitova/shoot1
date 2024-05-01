from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
 
        self.image = transform.scale(image.load(player_image), (size_x, size_y,))
        self.speed = player_speed
 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()

bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        global num_fire
        global rel_time
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            fire.play()
        
        
lost = 0
class Enemy(GameSprite):
    direction = 'down'
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(20, win_width - 80)
            lost += 1

class Asreroid(GameSprite):
    direction = 'down'
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(20, win_width - 80)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
win = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE!', True, (255, 30, 30))

player = Player('rocket.png', 320, 420, 65, 80, 4) 
asteroid = Asreroid('asteroid.png', randint(0, win_width - 80), 0, 85, 60, randint(1, 5))

game = True
finish = False
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play() 
fire = mixer.Sound('fire.ogg')

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(0, win_width - 80), 0, 85, 60, randint(1, 5))
    monsters.add(monster)

sprites_list = sprite.groupcollide(monsters, bullets, True, True )
hit = sprite.spritecollide(player, monsters, False)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    account = 0
    text_lost = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))

    window.blit(background,(0, 0))
    player.reset()
    asteroid.reset()
    monsters.draw(window)
    bullets.draw(window)

    sprites_list = sprite.groupcollide(monsters, bullets, True, True )
    hit = sprite.spritecollide(player, monsters, False)
    for sprite in sprites_list:
        account += 1
        monsters.add(monster)
    if account == 10:
        window.blit(win, (200, 200))
        finish = True
           
    if lost == 3:
        window.blit(lose, (200, 200))
        finish = True

    if hit or sprite.collide_rect(player, asteroid):
        window.blit(lose, (200, 200))
        finish = True

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.fire()
        monsters.update()
        bullets.update()
        asteroid.update()
        window.blit(text_lost, (0, 50))
        text_account = font1.render('Счёт:' + str(account), 1, (255, 255, 255))
        window.blit(text_account, (0, 20))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True )
        for sprite in sprites_list:
            account += 1
            monsters.add(monster)

        if account == 10:
            window.blit(win, (200, 200))
            finish = True
           
        if lost == 3:
            window.blit(lose, (200, 200))
            finish = True

        if hit or sprite.collide_rect(player, asteroid):
            window.blit(lose, (200, 200))
            finish = True

        player.reset()
        asteroid.reset()
        monsters.draw(window)
        bullets.draw(window)

    display.update()
    clock.tick(FPS)