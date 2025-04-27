from pygame import *
from assets import *
from random import randint

# (М5У10)
from record import *
from time import time as timer 
#імпортуємо функцію для засікання часу, щоб інтерпретатор 
# не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі

# фонова музика
mixer.init()
mixer.music.load(GAME_MUSIC)
mixer.music.play()
fire_sound = mixer.Sound(FIRE_SOUND)
damage_sound = mixer.Sound(DAMAGE_SOUND)

# нам потрібні такі картинки:
img_back = GAME_BG_IMG  # фон гри
img_hero = ROCKET_IMG  # герой
img_enemy = ENEMY_IMG # ворог
img_bullet = BULLET_IMG # куля 

# (М5У10)
img_enemy2 = ENEMY2_IMG # ворог 2

# шрифти і написи
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

score = 0  # збито кораблів
lost = 0  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки
goal = 10 # стільки кораблів потрібно збити для перемоги

# (М5У10)
life = 3  # очки життя
# рекорд очки
record = load_record()


# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
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
            
# (М5У10)
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.last_direction = "up"

    def update(self):
        keys = key.get_pressed()
        # if keys[K_LEFT] and self.rect.x > 5:
        #     self.rect.x -= self.speed
        # if keys[K_RIGHT] and self.rect.x < win_width - 80:
        #     self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.last_direction = "left"
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
            self.last_direction = "right"
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
            self.last_direction = "up"
        if keys[K_DOWN] and self.rect.y < win_height - 60:
            self.rect.y += self.speed
            self.last_direction = "down"
            
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15, self.last_direction) # y10= self.last_direction
        bullets.add(bullet)

# клас спрайта-ворога
class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    
# (М5У10)
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = direction

    def update(self):
        self.rect.y += self.speed
       

        # Якщо пуля вилетіла за видиме вікно - видаляємо її
        if self.rect.y < 0 or self.rect.y > win_height or self.rect.x < 0 or self.rect.x > win_width:
            self.kill()

# class Bullet(GameSprite):
    
#     def update(self):
#         self.rect.y += self.speed
#         # зникає, якщо дійде до краю екрана
#         if self.rect.y < 0:
#             self.kill()


# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# (М5У10)
# створення групи спрайтів-астероїдів
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_enemy2, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)



bullets = sprite.Group()


# ------------- (М5У9) -------------
start_time = time.get_ticks()  # час початку гри
shots_fired = 0  # кількість пострілів
# (М5У9)
def restart_game():
    global score, lost, finish, monsters, bullets, ship, start_time, shots_fired, num_fire, life, asteroids # (М5У10)
    score = 0
    lost = 0
    shots_fired = 0
    
    # (М5У10)
    num_fire = 0
    life = 3
    
    start_time = time.get_ticks()
    finish = False
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monsters = sprite.Group()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
    bullets = sprite.Group()
    # (М5У10)
    asteroids = sprite.Group()
    for i in range(1, 3):
        asteroid = Enemy(img_enemy2, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
        asteroids.add(asteroid)



finish = False
run = True

# (М5У10)
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів
max_bullets = 5

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        #подія натискання на пробіл - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                
                # (М5У10)
                if num_fire < max_bullets and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                    shots_fired += 1
                   
                if num_fire >= max_bullets and rel_time == False : #якщо гравець зробив 5 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки
                
            elif e.key == K_RETURN and finish:
                restart_game()


    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        # Обчислення таймера (у секундах)
        elapsed_time = (time.get_ticks() - start_time) // 1000
        timer_text = font2.render("Час: " + str(elapsed_time) + " с", 1, (255, 255, 255))
        window.blit(timer_text, timer_text.get_rect(topright=(win_width - 10, 20)))
        # Лічильник пострілів
        shots_text = font2.render("Постріли: " + str(shots_fired), 1, (255, 255, 255))
        window.blit(shots_text, shots_text.get_rect(topright=(win_width - 10, 50)))
        
        # (М5У10)
        record_text = font2.render("Рекорд: " + str(record), 1, (255, 255, 0))
        window.blit(record_text, (10, 80))


        # рухи спрайтів
        ship.update()
        monsters.update()
        asteroids.update()# (М5У10)
        bullets.update()

        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)# (М5У10)
        bullets.draw(window)
        
        
        # (М5У10)
        # перезарядка
        if rel_time == True:
            now_time = timer() # зчитуємо час
         
            if now_time - last_time < 3: #поки не минуло 3 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки


        
        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            
            # (М5У10)
            if score > record:
                record = score
                save_record(record)
        for monster in monsters:
            if monster.rect.x < 0:
                    monster.kill()
                    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                    monsters.add(monster)
        
        # Переробити!!
        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        # if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            # finish = True
            # window.blit(lose, (200, 200))
            # retry_text = font2.render("Натисність Enter, щоб почати спочатку", True, (255, 255, 255))
            # window.blit(retry_text, (100, 300))
        
        # (М5У10)
        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
        #програш
        if life == 0 or lost >= max_lost:
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
        # --------------------------
        
        
        # (М5У10)
        # задаємо різний колір залежно від кількості життів
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
       
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (10, 450))


        display.update()
        
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)
