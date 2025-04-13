from pygame import *
from assets import *
from random import randint
from record import*
from time import tima as timer

# фонова музика
mixer.init()
mixer.music.load(GAME_MUSIC)
mixer.music.play(-1)
fire_sound = mixer.Sound(FIRE_SOUND)

damage_sound = mixer.Sound(GAMAGE_SOUND)


# нам потрібні такі картинки:
img_back = GAME_BG_IMG  # фон гри
img_hero = ROCKET_IMG  # герой
img_enemy = ENEMY_IMG # ворог
img_bullet = BULLET_IMG # куля
img_enemy2 = ENEMY2_IMG

font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))

score = 0  # збито кораблів
lost = 0  # пропущено кораблів
max_lost = 8 # програли, якщо пропустили стільки

# (М5У9)
goal = 100 # стільки кораблів потрібно збити для перемоги

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, 
                 size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):

    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed



    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()        
bullets = sprite.Group()

  
   

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost  
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1 

        


# клас-батько для інших спрайтів

# клас головного гравця

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), 
                             (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


start_time = time.get_ticks()  # час початку гри
shots_fired = 0  # кількість пострілів
# (М5У9)
def restart_game():
    global score, lost, finish, monsters, bullets, ship, start_time, shots_fired
    score = 0
    lost = 0
    shots_fired = 0
    start_time = time.get_ticks()
    finish = False
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monsters = sprite.Group()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
    bullets = sprite.Group()


finish = False
run = True  # прапорець скидається кнопкою закриття вікна
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish: # (М5У9) added: `and not finish`
                fire_sound.play()
                ship.fire()
                # (М5У9)
                shots_fired += 1
                
            elif e.key == K_RETURN and finish:
                restart_game()      
    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущенно: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        # Обчислення таймера (у секундах)
        elapsed_time = (time.get_ticks() - start_time) // 1000
        timer_text = font2.render("Час: " + str(elapsed_time) + " с", 1, (255, 255, 255))
        window.blit(timer_text, timer_text.get_rect(topright=(win_width - 10, 20)))
        # Лічильник пострілів
        shots_text = font2.render("Постріли: " + str(shots_fired), 1, (255, 255, 255))
        window.blit(shots_text, shots_text.get_rect(topright=(win_width - 10, 50)))
        ship.update()
        monsters.update()
        monsters.draw(window)
        ship.reset()
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            retry_text = font2.render("Натисність Enter, щоб почати спочатку", True, (255, 255, 255))
            window.blit(retry_text, (100, 300))


        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            retry_text = font2.render("Натисність Enter, щоб почати спочатку", True, (255, 255, 255))
            window.blit(retry_text, (100, 300))
        display.update() 


        
        
        
        
    time.delay(50)
