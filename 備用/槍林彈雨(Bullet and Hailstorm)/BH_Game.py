import sys
import pygame
import random
import time
import os
import math
from pygame.sprite import Sprite

# 常數
FPS = 60  # frame per second, 統一遊戲運行次數
WIDTH = 600
HEIGHT = 600
bg_speed = 1

WHITE = (255, 255, 255)  # 參數分別是 red, green black 的色值
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# 遊戲初始化 & 視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()  # 管理遊戲運行時間的物件
current_time = time.time()
font_name = pygame.font.match_font("arial")  # match_font() 函式會載入電腦內已有的字體

# 圖檔
pause_img = pygame.image.load(os.path.join("image_for_game", "pause_page.png")).convert()
pause_img.set_colorkey(BLACK)
dead_img = pygame.image.load(os.path.join("image_for_game", "dead_page.png")).convert()
dead_img.set_colorkey(BLACK)
tutorial_img = pygame.image.load(os.path.join("image_for_game", "tutorial.png")).convert_alpha()
player_img = pygame.image.load(os.path.join("image_for_game", "player.png")).convert()
bullet_img = pygame.image.load(os.path.join("image_for_game", "bullet.png")).convert()  # 測試用圖檔
small_img = pygame.image.load(os.path.join("image_for_game", "small.png")).convert()
middle_img = pygame.image.load(os.path.join("image_for_game", "middle.png")).convert()
big_1_img = pygame.image.load(os.path.join("image_for_game", "big_level_1.png")).convert()
big_2_img = pygame.image.load(os.path.join("image_for_game", "big_level_2.png")).convert()
big_3_img = pygame.image.load(os.path.join("image_for_game", "big_level_3.png")).convert()
big_4_img = pygame.image.load(os.path.join("image_for_game", "big_level_4.png")).convert()
big_5_img = pygame.image.load(os.path.join("image_for_game", "big_level_5.png")).convert()
barrage_img = pygame.image.load(os.path.join("image_for_game", "barrage.png")).convert()
item_1_img = pygame.image.load(os.path.join("image_for_game", "item1.png")).convert()
item_2_img = pygame.image.load(os.path.join("image_for_game", "item2.png")).convert()
item_3_img = pygame.image.load(os.path.join("image_for_game", "item3.png")).convert()


class Background_item(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(tutorial_img, (WIDTH / 2, HEIGHT / 2))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = WIDTH / 2
        self.speed = bg_speed

    def update(self, *args):
        self.rect.bottom += self.speed

        # 一旦跑出畫面外，就要被移除
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.left > WIDTH
            or self.rect.right < 0
        ):
            self.kill()


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.image = pygame.transform.scale(player_img, (40, 40))
        self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20

        self.last_shot_time = pygame.time.get_ticks()  ##### 追蹤上次發射子彈的時間

        # 道具相關變數
        self.shoot_mode = 1  # 吃到道具後可以暫時改變
        self.speed_mode = 1  # 吃到道具後可以加速
        self.speed = 7 * self.speed_mode
        self.eat = False  # 判斷有沒有吃到道具，以及限制一次只能用一種道具
        self.item_timer = 0  # 用來計算吃到道具多久時間

        self.lives = 3

    def update(self, player):
        if (self.shoot_mode > 1 and pygame.time.get_ticks() - self.item_timer > 5000):  # 道具效果持續約五秒
            self.shoot_mode = 1
            self.item_timer = 0
            self.eat = False

        if self.speed_mode > 1 and pygame.time.get_ticks() - self.item_timer > 5000:
            self.speed_mode = 1
            self.item_timer = 0
            self.eat = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:  # 意思是 get_pressed() 回傳「右鍵」被按下了
            self.rect.centerx += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed
        if keys[pygame.K_UP]:
            self.rect.top -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.bottom += self.speed

        if self.rect.right >= WIDTH:  # 限制玩家的左右方向移動最多只到畫面兩邊
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 200:
            # 依據 shoot_mode 判斷不同射擊模式
            if self.shoot_mode == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.last_shot_time = current_time
                is_shooting = False
            elif self.shoot_mode == 2:  # 玩家暫時可以發射兩發子彈
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                self.last_shot_time = current_time

    def reposition(self, center):  # 碰撞到敵機，玩家就要被撞開，不然無法正常判斷與敵機的碰撞(這個函式之後要改)
        self.rect.centerx = center
        self.rect.bottom = HEIGHT

    def gun_up(self):
        self.eat = True
        self.shoot_mode += 1
        self.item_timer = pygame.time.get_ticks()  # 記下當前時間，之後用來計時

    def speed_up(self):
        self.eat = True
        self.speed_mode = 1.5
        self.item_timer = pygame.time.get_ticks()


class Bullet(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # 載入圖檔
        self.image = pygame.transform.scale(bullet_img, (20, 40))
        self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self, player):
        self.rect.bottom += self.speed

        # 一旦跑出畫面外，就要被移除
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.left > WIDTH
            or self.rect.right < 0
        ):
            self.kill()


class Item(Sprite):
    def __init__(self, enemy, level):
        Sprite.__init__(self)
        # 之後要給道具上圖檔
        # 判斷道具類型
        if level <= 2:  # 到 level 3 之前，道具最多兩種
            self.type = random.randrange(1, 1 + level)
            if self.type == 1:  # level 1 只能拿到這種道具
                self.image = pygame.transform.scale(item_1_img, (30, 30))
                self.image.set_colorkey(BLACK)
            elif self.type == 2:
                self.image = pygame.transform.scale(item_2_img, (30, 30))
                self.image.set_colorkey(BLACK)
        elif level > 2:  # level 3 開始，道具變成最多三種
            self.type = random.randrange(1, 4)
            if self.type == 1:
                self.image = pygame.transform.scale(item_1_img, (30, 30))
                self.image.set_colorkey(BLACK)
            elif self.type == 2:
                self.image = pygame.transform.scale(item_2_img, (30, 30))
                self.image.set_colorkey(BLACK)
            elif self.type == 3:
                self.image = pygame.transform.scale(item_3_img, (30, 30))
                self.image.set_colorkey(BLACK)

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = enemy.rect.centerx
        self.rect.bottom = enemy.rect.bottom

        # 道具的墜落速度
        self.speed_y = 3
        self.speed_x = random.randrange(-3, 4)

    def update(self, player):
        self.rect.bottom += self.speed_y
        self.rect.centerx += self.speed_x

        # 一旦跑出畫面外，就要被移除
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.left > WIDTH
            or self.rect.right < 0
        ):
            self.kill()


class SmallEnemy(Sprite):
    def __init__(self, level):
        Sprite.__init__(self)
        # 載入圖檔
        # 之後或許可以比照「生成位置的變動」，依據不同 level 給敵機不同的圖檔(以及不同移動模式)
        self.image = pygame.transform.scale(small_img, (40, 40))
        self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明

        self.last_shot_time = pygame.time.get_ticks()  # 追蹤上次發射子彈的時間

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # 賦予定位的框架，rect 可以用來定位

        self.speed = random.uniform(1.5, 3)
        self.direction = random.choice([1, -1])
        self.initial_angle = random.choice([0, 180])
        self.start_moved_time = time.time()
        self.duration = random.uniform(8, 15)
        self.moved_mode = level

        # 敵機的生成位置可以用 if 判斷當前的 level 後調整
        if level == 1:  # level 1 小型敵機只會從最上方生成
            self.rect.bottom = random.randrange(-20, -10)
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
        elif level == 2 or level == 3 or level == 4:  # 小型敵機開始可以從左右兩邊生成
            if len(small_enemies) <= level:  # 如果當前小型敵機數量低於 level
                dice = random.randrange(1, 7 - level)
                if dice == 1:  # 小型敵機從右邊生成
                    self.rect.bottom = random.randrange(100 * (level - 1), HEIGHT)
                    self.rect.centerx = WIDTH + self.rect.width
                elif dice == 2:  # 小型敵機從左邊生成
                    self.rect.bottom = random.randrange(100 * (level - 1), HEIGHT)
                    self.rect.centerx = 0 - self.rect.width
                else:  # 從最上方生成，level 4 就只會從左右兩邊生成
                    self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
                    self.rect.bottom = random.randrange(-20, -10)
        elif level >= 5:  # level 5 開始不只會從左右兩邊生成，還會從最下方跑上來
            dice = random.randrange(1, 4)
            if dice == 1:  # 從最下方生成
                self.rect.bottom = random.randrange(
                    HEIGHT + self.rect.height + 10, HEIGHT + self.rect.height + 20
                )
                self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            elif dice == 2:
                self.rect.bottom = random.randrange(200, HEIGHT)
                self.rect.centerx = WIDTH + self.rect.width
            elif dice == 3:
                self.rect.bottom = random.randrange(200, HEIGHT)
                self.rect.centerx = 0 - self.rect.width

        # 敵機的生命值
        self.original_lives = 3  # 這個變數會在繪製敵機生命值時用到，不能改
        self.lives = 3  # 敵機被射中後，變動的會是這個變數

        # 敵機的碰撞判斷相關的變數
        self.can_hit = True  # 跟玩家碰撞一次後，暫時讓物件變得無法跟玩家碰撞，以避免「多次碰撞」
        self.hit_timer = 0  # 計時器，等一定時間後再讓物件變得能跟玩家碰撞

    def update(self, player):
        # 移動方式
        moved_time = time.time() - self.start_moved_time
        if self.moved_mode == 1:
            if moved_time <= self.duration:
                angle = 90 * (moved_time / self.duration)
            else:
                angle = 90
            if self.initial_angle == 0:
                self.rect.centerx +=  0.5 * self.direction * self.speed * math.cos(math.radians(angle))
            elif self.initial_angle == 180:
                self.rect.centerx +=  0.5 * self.speed * math.cos(math.radians(self.initial_angle - angle))
            self.rect.centery += self.speed * math.sin(math.radians(angle))
        if self.moved_mode >= 2:
            if moved_time <= self.duration:
                angle = 90 * (moved_time / self.duration)
            elif moved_time > self.duration:
                self.speed = random.uniform(2, 4)
                self.direction = random.choice([1, -1])
                self.initial_angle = random.randrange(0, 360)
                self.start_moved_time = time.time()
                self.duration = random.uniform(8, 15)
            angle = 90 * (moved_time / self.duration)
            self.rect.centerx +=  0.5 * self.direction * self.speed * math.cos(math.radians(angle))
            self.rect.centery += self.speed * math.sin(math.radians(angle))


        # 超出邊界就重置
        if (
            self.rect.bottom > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0
        ):
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.rect.top = random.randrange(-100, -40)

        
    def shoot(self):
        shot_time = pygame.time.get_ticks()
        dx = 0
        dy = 3
        damage = 1
        if shot_time - self.last_shot_time >= 2000:  # 控制每隔2秒發射一次
            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
            all_sprites.add(barrage)
            barrages.add(barrage)
            self.last_shot_time = shot_time


class MiddleEnemy(Sprite):
    def __init__(self, level):
        Sprite.__init__(self)

        self.image = pygame.transform.scale(middle_img, (70, 70))
        self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明

        self.last_shot_time = pygame.time.get_ticks()  ##### 追蹤上次發射子彈的時間

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.speed = 2
        self.frame = 5
        # 敵機的生成位置
        if level == 1 or level == 2:  # level 1 和 2 中型敵機只會從最上方生成
            self.rect.bottom = random.randrange(-20, -10)
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
        elif level == 3:
            dice = random.randrange(1, 5)
            if dice == 1:  # 小型敵機從右邊生成
                self.rect.bottom = random.randrange(200, 500)
                self.rect.centerx = WIDTH + self.rect.width
            elif dice == 2:  # 小型敵機從左邊生成
                self.rect.bottom = random.randrange(200, 500)
                self.rect.centerx = 0 - self.rect.width
            else:
                self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
                self.rect.bottom = random.randrange(-20, -10)
        elif level >= 4:
            dice = random.randrange(1, 3)
            if dice == 1:  # 小型敵機從右邊生成
                self.rect.bottom = random.randrange(200, HEIGHT)
                self.rect.centerx = WIDTH + self.rect.width
            elif dice == 2:  # 小型敵機從左邊生成
                self.rect.bottom = random.randrange(200, HEIGHT)
                self.rect.centerx = 0 - self.rect.width

        self.original_lives = 6  # 這個變數會在繪製敵機生命值時用到，不能改
        self.lives = 6

        self.can_hit = True
        self.hit_timer = 0  # 計時器，等一定時間後再讓物件變得能跟玩家碰撞

    def update(self, player):
        # 移動方式
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > self.frame:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
        self.rect.centerx += dx
        self.rect.centery += dy
        if (
            self.rect.top > WIDTH or self.rect.left > WIDTH or self.rect.right < 0
        ):  # 超出邊界就重置位置
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.rect.top = random.randrange(-100, -40)

    def shoot(self, player):
        current_time = pygame.time.get_ticks()
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        speed = 3
        damage = 1
        if distance > self.frame:
            dx = (dx / distance) * speed
            dy = (dy / distance) * speed
        if current_time - self.last_shot_time >= 1500:  # 控制每隔1.5秒發射一次
            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
            all_sprites.add(barrage)
            barrages.add(barrage)
            self.last_shot_time = current_time
        if self.lives <= 0:
            for angle in range(0, 360, 60):  # 6個
                dx = math.cos(math.radians(angle)) * speed
                dy = math.sin(math.radians(angle)) * speed
                barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                all_sprites.add(barrage)
                barrages.add(barrage)


class BigEnemy(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        global level
        if level == 1:
            self.image = pygame.transform.scale(big_1_img, (100, 100))
            self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明
        elif level == 2:
            self.image = pygame.transform.scale(big_2_img, (100, 100))
            self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明
        elif level == 3:
            self.image = pygame.transform.scale(big_3_img, (100, 100))
            self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明
        elif level == 4:
            self.image = pygame.transform.scale(big_4_img, (100, 100))
            self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明
        elif level == 5:
            self.image = pygame.transform.scale(big_5_img, (100, 100))
            self.image.set_colorkey(BLACK)  # 把圖檔中黑色部分變透明

        self.start_shot_time = time.time()
        self.last_shot_time = pygame.time.get_ticks()

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.moved_mode = random.choice([1, 2, 3, 4, 5]) # 1~5 主移動方式

        self.rect = self.image.get_rect()  # rect 可以用來定位
        if self.moved_mode == 4:
            self.rect.centerx = random.choice([0 - self.rect.width, WIDTH + self.rect.width])
            self.rect.centery = random.randrange(HEIGHT/2 - 10, HEIGHT/2 + 10)
        elif self.moved_mode == 5:
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT + self.rect.height + 10
        else:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-20, -10)

        self.original_lives = 9  # 這個變數會在繪製敵機生命值時用到，不能改
        self.lives = 9

        self.can_hit = True
        self.hit_timer = 0  # 計時器，等一定時間後再讓物件變得能跟玩家碰撞

        self.speed = 3
        if self.moved_mode == 1:
            self.initial_angle = random.choice([30, 150])
        elif self.moved_mode == 4:
            self.initial_angle = -90
        elif self.moved_mode == 5:
            self.initial_angle = -90

        self.direction = random.choice([1, -1])
        self.start_moved_time = time.time()
        self.count = 0
        self.shot_mode = 1 # 次移動方式，必須由1開始循環
        self.positionx = 0
        self.positiony = 0
        self.frame = 5

    def update(self, player):
        # 移動方式
        if self.moved_mode == 1:
            self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
            if self.shot_mode == 1:
                self.rect.x += self.speed * self.direction
                if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width: # 定位x的來回
                    self.direction *= -1
                    self.count += 0.5
                elif self.count == 2:
                    self.shot_mode = 2
                    self.count = 0
                if self.positiony - self.rect.centery > self.frame: # 定位y
                    self.rect.centery += 0.5 * self.speed
                elif self.positiony - self.rect.centery  <= self.frame:
                    self.rect.centery = self.positiony
            elif self.shot_mode == 2:
                if self.rect.centerx - self.positionx > self.frame: # 定位x，y不動 
                    self.rect.centerx -= self.speed
                elif self.positionx - self.rect.centerx > self.frame:
                    self.rect.centerx += self.speed
                else:
                    self.rect.centerx = self.positionx
        elif self.moved_mode == 2:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 2:
                self.positionx, self.positiony = (75, HEIGHT - 75) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 3:
                self.positionx, self.positiony = (WIDTH - 75, HEIGHT - 75) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
        elif self.moved_mode == 3:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 2: # 順時針
                self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
                radiusx = WIDTH/2 - (self.rect.width/2 + 10)
                radiusy = HEIGHT/2 - (self.rect.height/2 + 10)
                moved_time = time.time() - self.start_moved_time
                duration = 30
                if moved_time <= duration:
                    angle = 360 * (moved_time / duration) - 90
                    self.rect.centerx = WIDTH/2 + math.cos(math.radians(angle)) * radiusx
                    self.rect.centery = HEIGHT/2 + math.sin(math.radians(angle)) * radiusy
                else:
                    self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 3: # 逆時針
                self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
                radiusx = WIDTH/2 - (self.rect.width/2 + 10)
                radiusy = HEIGHT/2 - (self.rect.height/2 + 10)
                moved_time = time.time() - self.start_moved_time
                duration = 30
                if moved_time <= duration:
                    angle = -360 * (moved_time / duration) - 90
                    self.rect.centerx = WIDTH/2 + math.cos(math.radians(angle)) * radiusx
                    self.rect.centery = HEIGHT/2 + math.sin(math.radians(angle)) * radiusy
                else:
                    self.rect.center = (self.positionx, self.positiony)
        elif self.moved_mode == 4:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH/2, HEIGHT/2) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 2 or self.shot_mode == 3:
                self.positionx, self.positiony = (WIDTH/2, self.rect.height/2 + 10) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
        elif self.moved_mode == 5:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH/2, HEIGHT - (self.rect.height + 10)) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 2:
                self.positionx, self.positiony = (WIDTH/2, self.rect.height + 10) # 特別定位
                if self.rect.center != (self.positionx, self.positiony): # 定位x和y
                    dx = self.positionx - self.rect.centerx
                    dy = self.positiony - self.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > self.frame:
                        dx = (dx / distance) * self.speed
                        dy = (dy / distance) * self.speed
                        self.rect.centerx += dx
                        self.rect.centery += dy
                    elif distance <= self.frame:
                        self.rect.center = (self.positionx, self.positiony)
                

    def shoot(self, player):
        speed = 5
        damage = 1
        if self.moved_mode == 1:
            if  self.shot_mode == 1:
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 1000:  # 控制每隔1.0秒發射一次
                    for i in [-40, 0, 40]:
                        dx = 0
                        dy = speed
                        barrage = Barrage(self.rect.centerx + i, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                    self.last_shot_time = start_shot_time
            elif self.shot_mode == 2 and self.rect.centerx == self.positionx:
                duration = 3
                radian = 120
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 100:  # 控制每隔0.1秒發射一次
                    if shot_time < duration:
                        angle = radian * (shot_time / duration)
                        if self.initial_angle == 90 - radian/2:
                            dx = speed * math.cos(math.radians(self.initial_angle + angle))
                            dy = speed * math.sin(math.radians(self.initial_angle + angle))
                        elif self.initial_angle == 90 + radian/2:
                            dx = speed * math.cos(math.radians(self.initial_angle - angle))
                            dy = speed * math.sin(math.radians(self.initial_angle - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        if self.initial_angle == 90 - radian/2:
                            self.initial_angle += radian
                        elif self.initial_angle == 90 + radian/2:
                            self.initial_angle -= radian
                        self.count += 0.5
                        self.start_shot_time = time.time()
                if self.count == 3:
                    self.shot_mode = 1
                    self.count = 0
        elif self.moved_mode == 2:
            if self.shot_mode == 1 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 200:
                    if shot_time < duration:
                        for angle in range(30, 150 + 1, 30): # 5個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        self.shot_mode = 2
                        self.start_shot_time = time.time()
            elif self.shot_mode == 2 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 200:
                    if shot_time < duration:
                        for angle in range(270, 360 + 1, 30): # 4個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.right, self.rect.top, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        self.shot_mode = 3
                        self.start_shot_time = time.time()
            elif self.shot_mode == 3 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 200:
                    if shot_time < duration:
                        for angle in range(180, 270 + 1, 30): # 4個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.left, self.rect.top, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        self.shot_mode = 1
                        self.start_shot_time = time.time()
        elif self.moved_mode == 3:
            if self.shot_mode == 1 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if shot_time < duration:
                    if start_shot_time - self.last_shot_time >= 200:
                        for angle in range(30, 150 + 1, 40): # 4個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                elif shot_time >= duration:
                    self.shot_mode = random.choice([2, 3])
                    self.last_shot_time = start_shot_time
                    self.start_moved_time = time.time()
            elif self.shot_mode == 2 or self.shot_mode == 3:
                start_shot_time = pygame.time.get_ticks()
                if start_shot_time - self.last_shot_time >= 200:
                    if self.rect.centerx > self.positionx + self.frame:
                        for angle in range(200, 250 + 1, 25): # 3個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.left, self.rect.top, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif self.rect.centerx < self.positionx - self.frame:
                        for angle in range(290, 340 + 1, 25): # 3個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.right, self.rect.top, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif math.dist(self.rect.center, (self.positionx, self.positiony)) < self.frame:
                        self.shot_mode = 1
                        self.rect.center = (self.positionx, self.positiony)  
                        self.start_moved_time = time.time()    
        elif self.moved_mode == 4:
            if self.shot_mode == 1 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 200:
                    if shot_time < duration:
                        for angle in range(0, 360, 45): # 8個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        self.shot_mode = 2
                        self.start_shot_time = time.time()
            elif self.shot_mode == 2 and self.rect.center == (self.positionx, self.positiony):
                duration = 0.5
                radian = 360
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 62.5:  # 控制每隔0.0625秒發射一次，所以一圈0.5秒
                    if shot_time < duration:
                        angle = radian * (shot_time / duration)
                        if self.initial_angle == 90 - radian/2: # -90
                            dx = speed * math.cos(math.radians(self.initial_angle + angle))
                            dy = speed * math.sin(math.radians(self.initial_angle + angle))
                        elif self.initial_angle == 90 + radian/2: # 270
                            dx = speed * math.cos(math.radians(self.initial_angle - angle))
                            dy = speed * math.sin(math.radians(self.initial_angle - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time <= duration + 1:
                        None
                    else:
                        if self.initial_angle == 90 - radian/2:
                            self.initial_angle += radian
                        elif self.initial_angle == 90 + radian/2:
                            self.initial_angle -= radian
                        self.start_shot_time = time.time()            
        elif self.moved_mode == 5:
            if self.shot_mode == 1 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                radian = 45
                delay_time = 3
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 100:
                    if shot_time - delay_time < 0: # 停滯
                        None
                    elif shot_time - delay_time < duration:
                        angle = radian * ((shot_time - delay_time) / duration) # 右邊
                        dx = speed * math.cos(math.radians(self.initial_angle + radian - angle))
                        dy = speed * math.sin(math.radians(self.initial_angle + radian - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        angle = radian * ((shot_time - delay_time) / duration) # 左邊
                        dx = speed * math.cos(math.radians(self.initial_angle - radian + angle))
                        dy = speed * math.sin(math.radians(self.initial_angle - radian + angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time - delay_time >= duration:
                        self.shot_mode = 2
                        self.start_shot_time = time.time()
            elif self.shot_mode == 2 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                delay_time = 3
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 100:
                    if shot_time - delay_time < 0:
                        None
                    elif shot_time - delay_time < duration:
                        for angle in range(0, 180 + 1, 15): # 12個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time - delay_time >= duration:
                        self.shot_mode = 1
                        self.start_shot_time = time.time()

        if self.lives <= 0:
            for angle in range(0, 360, 30):  # 12個
                dx = math.cos(math.radians(angle)) * speed
                dy = math.sin(math.radians(angle)) * speed
                barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                all_sprites.add(barrage)
                barrages.add(barrage)


class Barrage(Sprite):
    def __init__(self, x, y, dx, dy, damage):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(barrage_img, (30, 30))
        self.image.set_colorkey(BLACK)

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = dx
        self.speedy = dy
        self.damage = damage

    def update(self, player):
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx

        # 一旦跑出畫面外，就要被移除
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.left > WIDTH
            or self.rect.right < 0
        ):
            self.kill()


def draw_text(surf, text, size, x, y):  # 首先把當前的 level 寫出來好了
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # 把 text 當成平面渲染
    text_rect = text_surface.get_rect()  # 跟物件一樣, 取得定位的框架
    text_rect.centerx = x  # 定位文字
    text_rect.top = y
    surf.blit(text_surface, text_rect)  # 在傳進來的平面上畫上渲染出的 text_surface, 位置則是 text_rect


def draw_enemy_lives(enemy):  # 這函式應該要寫在下面的 更新遊戲 部分，且大概是要放在 update() 底下
    for e in enemy:  # 遍歷敵機當前群組中的所有敵機
        bar_length = e.rect.width
        bar_height = 5
        fill = bar_length * (e.lives / e.original_lives)
        outline_rect = pygame.Rect(
            e.rect.left, e.rect.bottom + 5, bar_length, bar_height
        )
        fill = pygame.Rect(e.rect.left, e.rect.bottom + 5, fill, bar_height)
        pygame.draw.rect(
            screen, RED, outline_rect, 1
        )  # 最後一個參數可以設定此矩形的像素，設定成 1 的話就會畫出矩形細線
        pygame.draw.rect(screen, RED, fill)


def draw_init():
    screen.fill(BLUE)  # 暫時先用藍色代表起始 UI
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():  # event.get() 會回傳現在發生的所有事件(包括滑鼠滑到哪、按下某按鍵等)
            if event.type == pygame.QUIT:
                sys.exit()  # 直接結束「程式運作」
            if (
                event.type == pygame.KEYDOWN
            ):  # 若 get() 回傳某按鍵「被按下」然後「被鬆開」, 就會讓 waiting 為 False
                waiting = False


def draw_pause():  # 遊戲迴圈內偵測到使用者按下 p 鍵，就會繪製 pause UI
    global paused, show_init
    screen.blit(pause_img, (155, 155))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 直接結束「程式運作」
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
                    paused = not paused  # 切換 pause 狀態
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False
                    show_init = True
                    paused = not paused


def draw_dead():  # 玩家 lives 屬性數值低於零就會顯示輸掉的畫面
    global dead
    if dead:
        screen.blit(dead_img, (155, 155))
        pygame.display.update()


def draw_tutorial():
    bg = Background_item()
    all_sprites.add(bg)


def new_small(level):
    se = SmallEnemy(level)
    all_sprites.add(se)
    small_enemies.add(se)


def new_middle(level):
    me = MiddleEnemy(level)
    all_sprites.add(me)
    middle_enemies.add(me)


def new_big():
    be = BigEnemy()
    all_sprites.add(be)
    big_enemies.add(be)


def new_item(enemy, level):  # 基本上，只有在打死中型敵機後才會掉道具
    i = Item(enemy, level)
    all_sprites.add(i)
    items.add(i)


def check_collision(sprite1, sprite2):  # 用來判斷 sprite 物件之間是否有碰撞
    offset_x = sprite2.rect.x - sprite1.rect.x  # 用來校準 mask 碰撞判斷的定位
    offset_y = sprite2.rect.y - sprite1.rect.y
    result = sprite1.mask.overlap(sprite2.mask, (offset_x, offset_y))
    return result is not None  # 若 result 不為空就回傳 result


# 遊戲迴圈
running = True
show_init = True  # 之後要用來決定是否顯示起始畫面的變數
paused = False  # 玩家按下 p 鍵(暫定，但可以改)時，遊戲會暫停並顯示 pause UI
dead = False  # 玩家死掉時就會跳出輸掉的畫面

frame_counter = 0  # 每次遊戲循環給計數器加 1
collision_check_threshold = 3  # 設定成每 3 幀檢查一次碰撞，減少碰撞判斷的計算次數

while running:
    if show_init:  # 判斷是否顯示起始畫面
        draw_init()  # 先畫出起始 UI

        show_init = False
        dead = False

        level = 1  # 用來改變關卡，同時此變數會改變敵機的生成方式

        small_death = 0
        middle_death = 0

        middle_make = False  # 小型敵機死一定數量就會生成中型敵機
        big_make = False  # 中型敵機死一定數量就會生成大型敵機

        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        small_enemies = pygame.sprite.Group()
        middle_enemies = pygame.sprite.Group()
        big_enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        barrages = pygame.sprite.Group()
        items = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        player_group.add(player)

        # 之後要先讓「遊戲教學」的圖檔先滑下來後，才呼叫 new_small()
        draw_tutorial()
        new_small(level)  # 每次遊戲的最開始都會有一個小型敵機出現

    clock.tick(FPS)  # 到這裡為止都算遊戲的初始化

    # ******取得輸入******
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # 切換 pause 狀態
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.shoot()

    for small_enemy in small_enemies:
        small_enemy.shoot()

    for middle_enemy in middle_enemies:
        middle_enemy.shoot(player)

    for big_enemy in big_enemies:
        big_enemy.shoot(player)

    if not show_init and not dead and paused:  # 判斷是否顯示暫停畫面
        draw_pause()  # 暫停 UI

    if not show_init and dead:  # 判斷玩家是否死亡
        draw_dead()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_r:
                    show_init = True
                    # 移除所有群組底下的物件
                    player_group.empty()
                    small_enemies.empty()
                    middle_enemies.empty()
                    big_enemies.empty()
                    bullets.empty()
                    barrages.empty()
                    items.empty()
                    # del player_group, small_enemies, middle_enemies, big_enemies, bullets, barrages, items

    if middle_make:
        new_middle(level)
        middle_make = False
    if big_make:
        new_big()
        big_make = False

    if not paused and not dead:  # 玩家死掉或 pause 就會停止更新遊戲
        # ******更新遊戲******
        all_sprites.update(
            player
        )  # 這裡的 all_sprites.update() 和底下的 all_sprites.draw() 對應「更新 & 顯示」
        frame_counter += 1

        if frame_counter >= collision_check_threshold:  # 限制碰撞判斷的計算次數
            for b in bullets:
                for s in small_enemies:
                    if check_collision(b, s):  # 若 b 和 s 發生碰撞
                        b.kill()  # 子彈基本上一碰撞就要移除
                        if type(s) == SmallEnemy:
                            s.lives -= 1
                        if s.lives <= 0:
                            s.kill()  # 小型敵機的 lives 屬性數值低於零就移除
                            small_death += 1
                            if len(small_enemies) <= level:  # 限制畫面中小型敵機的生成數量
                                for i in range(
                                    0, random.randrange(1, 1 + level), 1
                                ):  # 這邊會讓小型敵機越打越多，可能要改
                                    new_small(level)
                            if small_death >= (
                                5 + level
                            ):  # 打死大於 5 + level 的小型敵機就會生成中型敵機
                                if (
                                    len(middle_enemies) < level
                                ):  # 每關同時間最多只會有 level 架中型敵機
                                    middle_make = True

            for b in bullets:
                for m in middle_enemies:
                    if check_collision(b, m):  # 若 b 和 m 發生碰撞
                        b.kill()
                        if type(m) == MiddleEnemy:
                            m.lives -= 1
                        if m.lives <= 0:
                            m.shoot(player)  #####
                            m.kill()
                            middle_death += 1
                            dice = random.randrange(
                                0, 5 + player.lives
                            )  # 玩家的 lives 越少，越容易掉道具
                            if dice == 1:
                                new_item(m, level)
                            if middle_death >= (
                                4 + level
                            ):  # 打死大於 4 + level 的中型敵機就會生成大型敵機
                                if len(big_enemies) == 0:
                                    big_make = True
                                    middle_death = 0

            for b in bullets:
                for be in big_enemies:
                    if check_collision(b, be):  # 若 b 和 be 發生碰撞
                        b.kill()
                        if type(be) == BigEnemy:
                            be.lives -= 1
                        if be.lives <= 0:
                            be.shoot(player)
                            be.kill()
                            level += 1

            for p in player_group:
                for s in small_enemies:
                    if check_collision(p, s):  # 若 p 和 s 發生碰撞
                        player.lives -= 1
                        if type(s) == SmallEnemy:
                            s.lives -= 3
                            s.can_hit = False  # 讓物件暫時變得無法碰撞
                            s.hit_timer = (
                                pygame.time.get_ticks()
                            )  # 計時器，等一定時間後再讓物件變得能跟玩家碰撞
                            player.reposition(
                                s.rect.centerx
                            )  # 玩家碰撞到敵機就會被撞開(之後要改如何更改玩家位置)

                        if s.lives <= 0:  # 當小型敵機的 lives 屬性數值歸零，將該小型敵機從群組中移除
                            s.kill()
                            small_death += 1
                            if len(small_enemies) <= level:
                                for i in range(0, random.randrange(1, 1 + level), 1):
                                    new_small(level)
                            if small_death >= (
                                5 + level
                            ):  # 打死大於 5 + level 的小型敵機就會生成中型敵機
                                if (
                                    len(middle_enemies) < level
                                ):  # 每關同時間最多只會有 level 架中型敵機
                                    middle_make = True

            for p in player_group:
                for m in middle_enemies:
                    if check_collision(p, m):  # 若 p 和 m 發生碰撞
                        player.lives -= 1
                        if type(m) == MiddleEnemy:
                            m.lives -= 3
                            m.can_hit = False
                            m.hit_timer = pygame.time.get_ticks()
                            player.reposition(m.rect.centerx)

                        if m.lives <= 0:
                            m.kill()
                            middle_death += 1
                            dice = random.randrange(
                                0, 5 + player.lives
                            )  # 玩家的 lives 越少，越容易掉道具
                            if dice == 1:
                                new_item(m, level)
                            if middle_death >= (
                                4 + level
                            ):  # 打死大於 4 + level 的中型敵機就會生成大型敵機
                                if len(big_enemies) == 0:
                                    big_make = True
                                    middle_death = 0

            for p in player_group:
                for b in big_enemies:
                    if check_collision(p, b):  # 若 p 和 b 發生碰撞
                        player.lives -= 1
                        if type(b) == BigEnemy:
                            b.lives -= 3
                            b.can_hit = False
                            b.hit_timer = pygame.time.get_ticks()
                            player.reposition(b.rect.centerx)
                        if b.lives <= 0:
                            b.kill()
                            level += 1

            for p in player_group:
                for br in barrages:
                    if check_collision(p, br):  # 若 p 和 br 發生碰撞
                        player.lives -= 1
                        br.kill()

            for p in player_group:
                for i in items:
                    if check_collision(p, i):  # 若 p 和 i 發生碰撞
                        i.kill()
                        if i.type == 1 and player.lives + 1 <= 3:  # 第一種道具能加血
                            player.lives += 1
                        elif i.type == 2 and not player.eat:  # 暫時改變玩家的射擊模式
                            player.gun_up()
                        elif i.type == 3 and not player.eat:  # 玩家移動加速
                            player.speed_up()

            frame_counter = 0  # 檢查碰撞判斷後就重置計數器

        for s in small_enemies:  # 把敵機的 can_hit 換回 True
            if not s.can_hit and (current_time - s.hit_timer) >= 5000:
                s.can_hit = True

        for m in middle_enemies:
            if not m.can_hit and (current_time - m.hit_timer) >= 5000:
                m.can_hit = True

        for b in big_enemies:
            if not b.can_hit and (current_time - b.hit_timer) >= 5000:
                b.can_hit = True

        if player.lives <= 0:  # 玩家生命值低於零
            # 或許可以改成先播放幾秒的特效之後才讓遊戲停止更新
            # 要加上對玩家 lives 呈現圖檔的更改
            # 玩家死掉，就會被移除(之後要加入死掉時的特效)
            player.kill()
            dead = True

        # ******畫面顯示******
        screen.fill(BLACK)  # 給 screen 填滿顏色
        all_sprites.draw(screen)  # 指定畫在 screen 平面上

        if small_enemies:  # 畫出敵機的 lives
            draw_enemy_lives(small_enemies)
        if middle_enemies:
            draw_enemy_lives(middle_enemies)
        if big_enemies:
            draw_enemy_lives(big_enemies)

        draw_text(screen, str(level), 15, WIDTH / 2, 10)  # 顯示當前關卡，這段之後要改(字體也可能要改)

        pygame.display.update()


pygame.quit()
