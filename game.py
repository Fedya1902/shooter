from pygame import *
from assets import *
from random import randint

mixer.init()
mixer.music.load(GAME_MUSIC)
mixer.music.play(-1)
fire_sound = mixer.Sound(FIRE_SOUND)

img_back = GAME_BG_IMG
img_hero = ROKCET_IMG
img_enemy = ENEMY_IMG

class GameSprite(sprite.Sprite)
    def __init__(self, player_image, player_x, player_y,
                 size_x, size_y, player_speed):
        
        sprite.Sprite.__init__(self)    
        self.image = transform.scale(
            image.load(player_image) , (size_x, size_y,))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x += self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        pass       

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transofrm.scale(image.load(img_back)), ((win_width_ win_height))  
((win_width_ win_height) )       

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
finish = False
run = False
while run:
    for e in event.get():                                    



        
