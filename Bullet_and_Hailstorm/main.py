import sys
import asyncio
import pygame
import random
import time
import os
import math
from pygame.sprite import Sprite


# 常數
FPS = 60  # frame per second, 統一遊戲運行次數
WIDTH = 460
HEIGHT = 600

WHITE = (255, 255, 255)  # 參數分別是 red, green black 的色值
BLACK = (0, 0, 0)
RED = (178, 34, 34)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

BACKGROUND_COLOR = (60, 0, 110)  # 用來繪製動畫的常數跟變數
LINES_COLOR = (150, 40, 160)
LINE_WIDTH = 2  # 直線寬度
INITIAL_LINE_GAP = 5  # 初始直線間隔
LINE_GAP_INCREMENT = 2
line_y = 0
line_number = 1
line_frame_count = 0  # 計數器，每 60 個 frame 就更改直線間隔一次

# 遊戲初始化 & 視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption('Bullet Hell')
clock = pygame.time.Clock()  # 管理遊戲運行時間的物件
current_time = time.time()
font_name = pygame.font.match_font('arial')  # match_font() 函式會載入電腦內已有的字體

bgm_volume = 0.5

# 圖檔
init_title = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'init_title.png')).convert_alpha(), (WIDTH, 180))
init_message = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'init_message.png')).convert_alpha(), (WIDTH, HEIGHT))
tutorial_img = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'tutorial.png')).convert_alpha(), (WIDTH * 0.7, HEIGHT * 0.7))
note_img = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'note.png')).convert_alpha(), (WIDTH, HEIGHT))
pause_img = pygame.image.load(os.path.join('image_for_game', 'pause_page.png')).convert_alpha()
dead_img = pygame.image.load(os.path.join('image_for_game', 'dead_page.png')).convert_alpha()
surface_for_lines = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'surface_lines.png')).convert_alpha(), (WIDTH, HEIGHT))

level_numbers = []
for i in range(1, 6, 1):
    num = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', f'level_{i}.png')).convert_alpha(), (40, 60))
    level_numbers.append(num)

player_lives_images = []
for i in range(0, 4, 1):
    lives = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', f'player_lives_{i}.png')).convert_alpha(), (60, 70))
    player_lives_images.append(lives)

player_img = pygame.image.load(os.path.join('image_for_game', 'player.png')).convert()
player_hurt_img = pygame.image.load(os.path.join('image_for_game', 'player_hurt.png')).convert()

special_bullet_width = 100
special_bullet_height = 100

SB_1_img = pygame.image.load(os.path.join('image_for_game', 'Special_Bullet_1.png')).convert()
special_bullet_1_images = []
while special_bullet_height < 1200:
    special_bullet_width += 50
    special_bullet_height += 50
    img = pygame.transform.scale(SB_1_img, (int(special_bullet_width), int(special_bullet_height)))
    img.set_colorkey(BLACK)
    special_bullet_1_images.append(img)

special_bullet_width = 80
special_bullet_height = 120

SB_2_img = pygame.image.load(os.path.join('image_for_game', 'Special_Bullet_2.png')).convert()
special_bullet_2_images = []
while special_bullet_height < 600:
    special_bullet_height += 50
    img = pygame.transform.scale(SB_2_img, (int(special_bullet_width), int(special_bullet_height)))
    img.set_colorkey(BLACK)
    special_bullet_2_images.append(img)

special_bullet_width = 100
special_bullet_height = 100

bullet_imgs = []
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'bullet.png')).convert(), (30, 40))
bullet_img.set_colorkey(BLACK)
bullet_imgs.append(bullet_img)
for i in range(1, 3, 1):
    img = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', f'bullet_break_{i}.png')).convert(), (30, 30))
    img.set_colorkey(BLACK)
    bullet_imgs.append(img)

small_img = pygame.image.load(os.path.join('image_for_game', 'small.png')).convert()
small_mini_img = pygame.transform.scale(small_img, (20, 20))
small_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(small_mini_img)  # 改變視窗圖示

small_hurt_img = pygame.image.load(os.path.join('image_for_game', 'small_hurt.png')).convert()
middle_img = pygame.image.load(os.path.join('image_for_game', 'middle.png')).convert()
middle_hurt_img = pygame.image.load(os.path.join('image_for_game', 'middle_hurt.png')).convert()
big_1_img = pygame.image.load(os.path.join('image_for_game', 'big_level_1.png')).convert()
big_1_img_hurt = pygame.image.load(os.path.join('image_for_game', 'big_level_1_hurt.png')).convert()
big_2_img = pygame.image.load(os.path.join('image_for_game', 'big_level_2.png')).convert()
big_2_img_hurt = pygame.image.load(os.path.join('image_for_game', 'big_level_2_hurt.png')).convert()
big_3_img = pygame.image.load(os.path.join('image_for_game', 'big_level_3.png')).convert()
big_3_img_hurt = pygame.image.load(os.path.join('image_for_game', 'big_level_3_hurt.png')).convert()
big_4_img = pygame.image.load(os.path.join('image_for_game', 'big_level_4.png')).convert()
big_4_img_hurt = pygame.image.load(os.path.join('image_for_game', 'big_level_4_hurt.png')).convert()
big_5_img = pygame.image.load(os.path.join('image_for_game', 'big_level_5.png')).convert()
big_5_img_hurt = pygame.image.load(os.path.join('image_for_game', 'big_level_5_hurt.png')).convert()
barrage_img = pygame.image.load(os.path.join('image_for_game', 'barrage.png')).convert()

explosion_img = []
for i in range(1, 5, 1):
    img = pygame.image.load(os.path.join('image_for_game', f'dead_animation_{i}.png')).convert()
    img.set_colorkey(BLACK)
    explosion_img.append(img)

block_img = []
for i in range(1, 8, 1):
    img = pygame.image.load(os.path.join('image_for_game', f'block_{i}.png')).convert()
    img.set_colorkey(BLACK)
    block_img.append(img)

items_img = []
for i in range(1, 9, 1):
    item = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', f'item{i}.png')).convert(), (40, 40))
    item.set_colorkey(BLACK)
    items_img.append(item)

ending_img = pygame.transform.scale(pygame.image.load(os.path.join('image_for_game', 'ending_text.png')).convert_alpha(), (WIDTH - 80, 200))

# 載入音檔
intro_bgm = os.path.join('sound_for_game', 'intro_music.wav')
normal_bgm_without_middle = os.path.join('sound_for_game', 'normal_bgm_without_middle.wav')
normal_bgm_with_middle = os.path.join('sound_for_game', 'normal_bgm_with_middle.wav')
boss_bgm_stage_1 = os.path.join('sound_for_game', 'boss_fight_1.wav')
boss_bgm_stage_2 = os.path.join('sound_for_game', 'boss_fight_2.wav')
boss_bgm_stage_3 = os.path.join('sound_for_game', 'boss_fight_3.wav')
player_shoot_sound = pygame.mixer.Sound(os.path.join('sound_for_game', 'player_shoot.wav'))
player_shoot_sound.set_volume(0.2)
enemy_laser_sound = pygame.mixer.Sound(os.path.join('sound_for_game', 'laser_beam.wav'))
enemy_laser_sound.set_volume(0.2)
enemy_explosion_sound = pygame.mixer.Sound(os.path.join('sound_for_game', 'explosion.wav'))
enemy_explosion_sound.set_volume(0.5)
item_get_sound = pygame.mixer.Sound(os.path.join('sound_for_game', 'item_get_sound.wav'))
item_get_sound.set_volume(0.5)


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        # 底下是用來顯示玩家圖檔跟特效用的
        self.images = [pygame.transform.scale(player_img, (30, 40)), pygame.transform.scale(player_hurt_img, (40, 40))]
        for i in self.images:
            i.set_colorkey(BLACK)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.flash_timer = None

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20

        self.last_shot_time = pygame.time.get_ticks()  # 追蹤上次發射子彈的時間

        # 道具相關變數
        self.shoot_mode = 1  # 吃到道具後可以暫時改變
        self.speed_mode = 1  # 吃到道具後射擊加速
        self.eat_shoot = False  # 有些道具不能同時起作用
        self.speed = 7
        self.item_timer = 0  # 用來計算吃到道具多久時間

        self.lives = 3

        self.can_hit = True  # 玩家碰撞後會短暫進入「不可碰撞」狀態
        self.hit_timer = None

    def update(self, *args):
        global win_game
        if not self.can_hit:
            self.flash_effect()  # 玩家被打中後會有特效
            if self.hit_timer is None:
                self.hit_timer = pygame.time.get_ticks()
            now = pygame.time.get_ticks()
            if now - self.hit_timer > 1000:  # 檢查是否超過 1 秒
                self.can_hit = True
                self.hit_timer = None
                self.image_index = 0

        now = pygame.time.get_ticks()
        if self.shoot_mode > 1 and now - self.item_timer > 8000:  # 道具效果持續約 8 秒
            self.shoot_mode = 1
            self.item_timer = 0
        if self.speed_mode > 1 and now - self.item_timer > 8000:
            self.speed_mode = 1
            self.item_timer = 0

        keys = pygame.key.get_pressed()

        if not win_game:
            if keys[pygame.K_d]:  # 意思是 get_pressed() 回傳「右鍵」被按下了
                self.rect.centerx += self.speed
            if keys[pygame.K_a]:
                self.rect.centerx -= self.speed
            if keys[pygame.K_w]:
                self.rect.top -= self.speed
            if keys[pygame.K_s]:
                self.rect.bottom += self.speed

            if self.rect.right >= WIDTH:  # 限制玩家的左右方向移動最多只到畫面兩邊
                self.rect.right = WIDTH
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top <= 0:
                self.rect.top = 0
        else:  # 使用者獲勝，遊戲結束
            if self.rect.centerx < WIDTH / 2:
                self.rect.centerx += 3
            if self.rect.centerx > WIDTH / 2:
                self.rect.centerx -= 3
            self.rect.bottom -= 1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 200 * (1/self.speed_mode):  # 控制每隔0.1秒發射一次
            # 依據 shoot_mode 判斷不同射擊模式
            if self.shoot_mode == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.last_shot_time = current_time #####
            elif self.shoot_mode == 2:  # 玩家暫時可以發射兩發子彈
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                self.last_shot_time = current_time
            elif self.shoot_mode in [3, 4, 5]:
                self.special_shoot()
            elif self.shoot_mode in [6, 7]:
                self.big_one()

    def special_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 200 * (1/self.speed_mode):  # 控制每隔0.1秒發射一次
            if self.shoot_mode == 3:  # 上下射擊
                bullet_1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet_1)
                bullets.add(bullet_1)

                bullet_2 = SpecialBullet(self)
                all_sprites.add(bullet_2)
                bullets.add(bullet_2)

                self.last_shot_time = current_time

            if self.shoot_mode == 4:  # 上下左右射擊
                bullet_1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet_1)
                bullets.add(bullet_1)

                bullet_2 = SpecialBullet(self, direction=1)  # 向左
                all_sprites.add(bullet_2)
                bullets.add(bullet_2)

                bullet_3 = SpecialBullet(self, direction=2)  # 向右
                all_sprites.add(bullet_3)
                bullets.add(bullet_3)

                bullet_4 = SpecialBullet(self, direction=3)  # 向右
                all_sprites.add(bullet_4)
                bullets.add(bullet_4)

                self.last_shot_time = current_time

            if self.shoot_mode == 5:  # 加上向下射擊兩發子彈
                bullet_1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet_1)
                bullets.add(bullet_1)

                bullet_2 = SpecialBullet(self, x=self.rect.left, y=self.rect.bottom)
                all_sprites.add(bullet_2)
                bullets.add(bullet_2)

                bullet_3 = SpecialBullet(self, x=self.rect.right, y=self.rect.bottom)
                all_sprites.add(bullet_3)
                bullets.add(bullet_3)

                self.last_shot_time = current_time

    def big_one(self):
        # 要確保「環狀」跟「大絕招」只會被生成一次
        if self.shoot_mode == 6:
            circle = SpecialBullet(self)
            all_sprites.add(circle)
            bullets.add(circle)
            self.shoot_mode = 1
        if self.shoot_mode == 7:
            big_one = SpecialBullet(self)
            all_sprites.add(big_one)
            bullets.add(big_one)
            self.shoot_mode = 1

    def flash_effect(self):  # 在玩家類別內的 update() 被呼叫
        if not self.can_hit:
            now = pygame.time.get_ticks()
            if self.flash_timer is None:
                self.flash_timer = now  # 紀錄當前時間(只會記下這麼一次，直到之後再次計時)
            if now - self.flash_timer > 1000:  # 當前時間跟 can_hit 開始變成 False 的時間紀錄的差距
                self.flash_timer = None
                self.image_index = 0
                self.can_hit = False
            elif (now - self.flash_timer) % 500 < 100:
                self.image_index = 1
            else:
                self.image_index = 0
            self.image = self.images[self.image_index]

    def gun_up(self, type):
        if type == 2:
            self.shoot_mode = 2
        if type == 4:
            self.shoot_mode = 3
        if type == 5:
            self.shoot_mode = 4
        if type == 6:
            self.shoot_mode = 5
        if type == 7:
            self.shoot_mode = 6
        if type == 8:
            self.shoot_mode = 7

        self.item_timer = pygame.time.get_ticks()  # 記下當前時間，之後用來計時

    def speed_up(self):
        self.speed_mode = 2
        self.item_timer = pygame.time.get_ticks()


class Bullet(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # 載入圖檔
        self.image_index = 0
        self.image = bullet_imgs[self.image_index]

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

        # 特效相關變數
        self.play_ani = False
        self.ani_timer = None

    def update(self, player):
        if not self.play_ani:
            self.rect.bottom += self.speed

        if self.play_ani:
            x = self.rect.centerx
            y = self.rect.centery
            self.image = bullet_imgs[self.image_index]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            now = pygame.time.get_ticks()
            if not self.ani_timer:
                self.ani_timer = now
            if now - self.ani_timer >= 10:  # 約 0.01 秒切換一次圖檔
                self.ani_timer = now
                if self.image_index < len(bullet_imgs) - 1:
                    self.image_index += 1
                    self.image = bullet_imgs[self.image_index]
                    if self.image_index == len(bullet_imgs) - 1:
                        self.kill()

        # 一旦跑出畫面外，就要被移除
        if self.rect.centery < 0:
            self.kill()


class SpecialBullet(Sprite):
    def __init__(self, p, x=None, y=None, direction=None):  # x,y,direction 可輸入可不輸入，預設為 None
        Sprite.__init__(self)
        global player

        self.type = p.shoot_mode

        # 載入圖檔
        if self.type == 3:  # 上下射擊
            # 載入圖檔
            self.image_index = 0
            self.image = pygame.transform.flip(bullet_imgs[self.image_index], False, True)  # 上下顛倒

            # 用來做碰撞判斷的 mask 屬性
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = p.rect.centerx
            self.rect.top = p.rect.centery
            self.speed = 10

            # 特效相關變數
            self.play_ani = False
            self.ani_timer = None

        if self.type == 4:  # 上下左右射擊
            if direction == 1:  # 1 為左
                # 載入圖檔
                self.image_index = 0
                self.image = pygame.transform.rotate(bullet_imgs[self.image_index], -90)  # 逆時針轉 90 度

                # 用來做碰撞判斷的 mask 屬性
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect()  # rect 可以用來定位
                self.rect.centerx = p.rect.centerx
                self.rect.top = p.rect.centery
                self.speed_x = -10
                self.speed_y = 0

            if direction == 2:  # 2 為右
                # 載入圖檔
                self.image_index = 0
                self.image = pygame.transform.rotate(bullet_imgs[self.image_index], 90)  # 順時針轉 90 度

                # 用來做碰撞判斷的 mask 屬性
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect()  # rect 可以用來定位
                self.rect.centerx = p.rect.centerx
                self.rect.top = p.rect.centery
                self.speed_x = 10
                self.speed_y = 0

            if direction == 3:  # 3 為下
                # 載入圖檔
                self.image_index = 0
                self.image = pygame.transform.flip(bullet_imgs[self.image_index], False, True)  # 上下顛倒

                # 用來做碰撞判斷的 mask 屬性
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect()  # rect 可以用來定位
                self.rect.centerx = p.rect.centerx
                self.rect.top = p.rect.centery
                self.speed_x = 0
                self.speed_y = 10

            # 特效相關變數
            self.play_ani = False
            self.ani_timer = None

        if self.type == 5:  # 加上兩發向下射擊的子彈
            # 載入圖檔
            self.image_index = 0
            self.image = pygame.transform.flip(bullet_imgs[self.image_index], False, True)  # 上下顛倒

            # 用來做碰撞判斷的 mask 屬性
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = x
            self.rect.top = y
            self.speed = 10

            # 特效相關變數
            self.play_ani = False
            self.ani_timer = None

        if self.type == 6:  # 環狀
            self.images = special_bullet_1_images  # 用來撥放「環狀」的動畫
            self.image_index_6 = 0
            self.image = self.images[self.image_index_6]
            self.mask = pygame.mask.from_surface(self.image)  # 之後在 update() 部分來還要更新 mask

            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = p.rect.centerx
            self.rect.centery = p.rect.centery

            self.scale_timer = pygame.time.get_ticks()

            self.circle_timer = pygame.time.get_ticks()

        if self.type == 7:  # 大絕招
            self.images = special_bullet_2_images  # 用來撥放「環狀」的動畫
            self.image_index_7 = 0
            self.image = self.images[self.image_index_7]
            self.mask = pygame.mask.from_surface(self.image)  # 之後在 update() 部分來還要更新 mask

            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = p.rect.centerx
            self.rect.centery = p.rect.top - 10

            self.scale_timer = pygame.time.get_ticks()

            self.big_one_timer = None

    def update(self, player):
        if self.type == 3 or self.type == 5:
            if not self.play_ani:
                self.rect.top += self.speed  # 向下移動

            # 一旦跑出畫面外，就要被移除
            if self.rect.centery < 0 or self.rect.centery > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
                self.kill()

        if self.type == 4:
            if not self.play_ani:
                self.rect.centerx += self.speed_x
                self.rect.centery += self.speed_y

            # 一旦跑出畫面外，就要被移除
            if self.rect.centery < 0 or self.rect.centery > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
                self.kill()

        if self.type in [3, 4, 5]:
            if self.play_ani:
                x = self.rect.centerx
                y = self.rect.centery
                self.image = bullet_imgs[self.image_index]
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.centery = y
                now = pygame.time.get_ticks()
                if not self.ani_timer:
                    self.ani_timer = now
                if now - self.ani_timer >= 10:  # 約 0.01 秒切換一次圖檔
                    self.ani_timer = now
                    if self.image_index < len(bullet_imgs) - 1:
                        self.image_index += 1
                        self.image = bullet_imgs[self.image_index]
                        if self.image_index == len(bullet_imgs) - 1:
                            self.kill()

        if self.type == 6:
            current_time = pygame.time.get_ticks()

            if current_time - self.scale_timer >= 100:  # 每 0.1 秒就切換圖檔
                self.scale_timer = current_time
                if self.image_index_6 < len(self.images):
                    self.image_index_6 += 1
                    if self.image_index_6 < len(self.images):
                        self.image = self.images[self.image_index_6]
                    else:
                        self.image_index_6 = len(self.images) - 1
                        self.image = self.images[self.image_index_6]
                # mask & rect 都獨立於 image 因此換了圖檔之後也要一起更新
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect(center=self.rect.center)

            # 一旦跑出畫面外，就要被移除
            if (self.rect.width / 2 > WIDTH) or (current_time - self.circle_timer >= 6000):
                self.kill()
                player.shoot_mode = 1

        if self.type == 7:
            current_time = pygame.time.get_ticks()
            if not self.big_one_timer:
                self.big_one_timer = current_time

            if current_time - self.scale_timer >= 100:  # 每 0.1 秒就增長
                self.scale_timer = current_time
                if self.image_index_7 < len(self.images):
                    self.image_index_7 += 1
                    if self.image_index_7 < len(self.images):
                        self.image = self.images[self.image_index_7]
                    else:
                        self.image_index_7 = len(self.images) - 1
                        self.image = self.images[self.image_index_7]
                # mask & rect 都獨立於 image 因此換了圖檔之後也要一起更新
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.bottom = player.rect.top - 10
                self.rect.centerx = player.rect.centerx

            if current_time - self.big_one_timer >= 6000:  # 大絕招持續約 6 秒
                self.kill()
                player.shoot_mode = 1


class SmallEnemy(Sprite):
    def __init__(self, level):
        Sprite.__init__(self)
        # 載入圖檔
        self.images = [pygame.transform.scale(small_img, (40, 40)), pygame.transform.scale(small_hurt_img, (30, 30))]
        for i in self.images:
            i.set_colorkey(BLACK)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.flash_timer = None

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
            self.rect.bottom = -10
            self.rect.centerx = random.randrange(50, WIDTH - self.rect.width - 50)
        elif level == 2 or level == 3 or level == 4:  # 小型敵機開始可以從左右兩邊生成
            if len(small_enemies) <= level:  # 如果當前小型敵機數量低於 level
                dice = random.randrange(1, 7-level)
                if dice == 1:  # 小型敵機從右邊生成
                    self.rect.bottom = random.randrange(100*(level-1), HEIGHT)
                    self.rect.centerx = WIDTH + self.rect.width
                elif dice == 2:  # 小型敵機從左邊生成
                    self.rect.bottom = random.randrange(100*(level-1), HEIGHT)
                    self.rect.centerx = 0 - self.rect.width
                else:  # 從最上方生成，level 4 就只會從左右兩邊生成
                    self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
                    self.rect.bottom = random.randrange(-20, -10)

        elif level >= 5:  # level 5 開始不只會從左右兩邊生成，還會從最下方跑上來
            dice = random.randrange(1, 4)
            if dice == 1:  # 從最下方生成
                self.rect.bottom = random.randrange(HEIGHT+self.rect.height+10, HEIGHT+self.rect.height+20)
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

        # 敵機的碰撞判斷以及特效相關的變數
        self.hit = False

        self.ani = [pygame.transform.scale(i, (self.rect.width, self.rect.height)) for i in explosion_img]
        self.ani_index = 0
        self.ani_timer = None

    def update(self, *args):
        # 移動方式
        moved_time = time.time() - self.start_moved_time
        if self.moved_mode == 1:
            if moved_time <= self.duration:
                angle = 90 * (moved_time / self.duration)
            else:
                angle = 90
            if self.initial_angle == 0:
                self.rect.centerx += 0.5 * self.direction * self.speed * math.cos(math.radians(angle))
            elif self.initial_angle == 180:
                self.rect.centerx += 0.5 * self.speed * math.cos(math.radians(self.initial_angle - angle))
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
            self.rect.centerx += 0.5 * self.direction * self.speed * math.cos(math.radians(angle))
            self.rect.centery += self.speed * math.sin(math.radians(angle))

        # 超出邊界就重置
        if self.rect.bottom > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.centerx = random.randrange(50, WIDTH - self.rect.width - 50)
            self.rect.top = 0 - self.rect.height

        if self.hit:
            self.flash_effect()

        # 死亡時撥放動畫
        if self.lives <= 0:
            self.image = self.ani[self.ani_index]
            now = pygame.time.get_ticks()
            if not self.ani_timer:
                self.ani_timer = now
            if now - self.ani_timer >= 10:  # 約 0.01 秒切換一次圖檔
                self.ani_timer = now
                if self.ani_index < len(self.ani) - 1:
                    self.ani_index += 1
                    self.image = self.ani[self.ani_index]
                    if self.ani_index == len(self.ani) - 1:
                        self.kill()

    def shoot(self):
        shot_time = pygame.time.get_ticks()
        dx = 0
        dy = 3
        damage = 1
        if shot_time - self.last_shot_time >= 2000:  # 控制每隔2秒發射一次
            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
            all_sprites.add(barrage)
            barrages.add(barrage)

            enemy_laser_sound.play()  # 音效

            self.last_shot_time = shot_time

    def flash_effect(self):
        if self.hit:
            now = pygame.time.get_ticks()
            if self.flash_timer is None:
                self.flash_timer = now
            if now - self.flash_timer > 1000:
                self.flash_timer = None
                self.image_index = 0
                self.hit = False
            elif (now - self.flash_timer) % 500 < 100:
                self.image_index = 1
            else:
                self.image_index = 0
            self.image = self.images[self.image_index]


class MiddleEnemy(Sprite):
    def __init__(self, level):
        Sprite.__init__(self)

        self.images = [pygame.transform.scale(middle_img, (70, 70)), pygame.transform.scale(middle_hurt_img, (70, 70))]
        for i in self.images:
            i.set_colorkey(BLACK)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.flash_timer = None

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

        # 敵機的碰撞判斷以及特效相關的變數
        self.hit = False

        self.ani = [pygame.transform.scale(i, (self.rect.width, self.rect.height)) for i in explosion_img]
        self.ani_index = 0
        self.ani_timer = None

        self.round_shoot = False

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

        if self.hit:
            self.flash_effect()

        # 死亡時撥放動畫
        if self.lives <= 0:
            self.image = self.ani[self.ani_index]
            now = pygame.time.get_ticks()
            if not self.ani_timer:
                self.ani_timer = now
            if now - self.ani_timer >= 10:  # 約 0.01 秒切換一次圖檔
                self.ani_timer = now
                if self.ani_index < len(self.ani) - 1:
                    self.ani_index += 1
                    self.image = self.ani[self.ani_index]
                    if self.ani_index == len(self.ani) - 1:
                        self.round_shoot = True

    def shoot(self, player):
        current_time = pygame.time.get_ticks()
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        speed = 3
        damage = 1
        if distance > self.frame:
            dx = (dx / distance) * speed
            dy = (dy / distance) * speed
        if current_time - self.last_shot_time >= 1500:  # 控制每隔1.5秒發射一次
            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
            all_sprites.add(barrage)
            barrages.add(barrage)

            enemy_laser_sound.play()  # 音效

            self.last_shot_time = current_time
        if self.round_shoot:
            for angle in range(0, 360, 60):  # 6個
                dx = math.cos(math.radians(angle)) * speed
                dy = math.sin(math.radians(angle)) * speed
                barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                all_sprites.add(barrage)
                barrages.add(barrage)
            self.kill()

    def flash_effect(self):
        if self.hit:
            now = pygame.time.get_ticks()
            if self.flash_timer is None:
                self.flash_timer = now
            if now - self.flash_timer > 1000:
                self.flash_timer = None
                self.image_index = 0
                self.hit = False
            elif (now - self.flash_timer) % 500 < 100:
                self.image_index = 1
            else:
                self.image_index = 0
            self.image = self.images[self.image_index]


class BigEnemy(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        global level
        if level == 1:
            self.images = [pygame.transform.scale(big_1_img, (120, 120)), pygame.transform.scale(big_1_img_hurt, (120, 120))]
            for i in self.images:
                i.set_colorkey(BLACK)

            self.image_index = 0
            self.image = self.images[self.image_index]

            self.moved_mode = 1
        elif level == 2:
            self.images = [pygame.transform.scale(big_2_img, (120, 120)),
                           pygame.transform.scale(big_2_img_hurt, (120, 120))]
            for i in self.images:
                i.set_colorkey(BLACK)

            self.image_index = 0
            self.image = self.images[self.image_index]

            self.moved_mode = 2
        elif level == 3:
            self.images = [pygame.transform.scale(big_3_img, (120, 120)),
                           pygame.transform.scale(big_3_img_hurt, (120, 120))]
            for i in self.images:
                i.set_colorkey(BLACK)

            self.image_index = 0
            self.image = self.images[self.image_index]

            self.moved_mode = 3
        elif level == 4:
            self.images = [pygame.transform.scale(big_4_img, (120, 120)),
                           pygame.transform.scale(big_4_img_hurt, (120, 120))]
            for i in self.images:
                i.set_colorkey(BLACK)

            self.image_index = 0
            self.image = self.images[self.image_index]

            self.moved_mode = 4
        elif level == 5:
            self.images = [pygame.transform.scale(big_5_img, (120, 120)),
                           pygame.transform.scale(big_5_img_hurt, (120, 120))]
            for i in self.images:
                i.set_colorkey(BLACK)

            self.image_index = 0
            self.image = self.images[self.image_index]

            self.moved_mode = 5

        self.start_shot_time = time.time()
        self.last_shot_time = pygame.time.get_ticks()

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # rect 可以用來定位
        if self.moved_mode == 4:
            self.rect.centerx = random.choice([0 - self.rect.width, WIDTH + self.rect.width])
            self.rect.centery = random.randrange(int(HEIGHT/2 - 10), int(HEIGHT/2 + 10))
        elif self.moved_mode == 5:
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT + self.rect.height + 10
        else:
            self.rect.centerx = random.randrange(0 + self.rect.width, WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-20, -10)

        # 大型敵機生命值，依據當前 level 改變，越後面越難打
        self.original_lives = 60 * level  # 這個變數會在繪製敵機生命值時用到，不能改
        self.lives = 60 * level

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
        self.shot_mode = 1  # 次移動方式，必須由1開始循環
        self.positionx = 0
        self.positiony = 0
        self.frame = 5

        # 敵機的碰撞判斷以及特效相關的變數
        self.hit = False
        self.hit_timer = None

        self.ani = [pygame.transform.scale(i, (self.rect.width, self.rect.height/2)) for i in explosion_img]
        self.ani_index = 0
        self.ani_timer = None

        self.round_shoot = False

    def update(self, player):
        global level
        if self.hit:
            now = pygame.time.get_ticks()
            if not self.hit_timer:
                hit_timer = now
            if now - hit_timer >= 1000:
                self.hit = False

        # 移動方式
        if self.moved_mode == 1:
            self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
            if self.shot_mode == 1:
                self.rect.x += self.speed * self.direction
                if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:  # 定位x的來回
                    self.direction *= -1
                    self.count += 0.5
                elif self.count == 2:
                    self.shot_mode = 2
                    self.count = 0
                if self.positiony - self.rect.centery > self.frame:  # 定位y
                    self.rect.centery += 0.5 * self.speed
                elif self.positiony - self.rect.centery <= self.frame:
                    self.rect.centery = self.positiony
            elif self.shot_mode == 2:
                if self.rect.centerx - self.positionx > self.frame:  # 定位x，y不動
                    self.rect.centerx -= self.speed
                elif self.positionx - self.rect.centerx > self.frame:
                    self.rect.centerx += self.speed
                else:
                    self.rect.centerx = self.positionx
        elif self.moved_mode == 2:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (75, HEIGHT - 75)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (WIDTH - 75, HEIGHT - 75)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
            elif self.shot_mode == 2:  # 順時針
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
                radiusx = WIDTH / 2 - (self.rect.width / 2 + 10)
                radiusy = HEIGHT / 2 - (self.rect.height / 2 + 10)
                moved_time = time.time() - self.start_moved_time
                duration = 30
                if moved_time <= duration:
                    angle = 360 * (moved_time / duration) - 90
                    self.rect.centerx = WIDTH / 2 + math.cos(math.radians(angle)) * radiusx
                    self.rect.centery = HEIGHT / 2 + math.sin(math.radians(angle)) * radiusy
                else:
                    self.rect.center = (self.positionx, self.positiony)
            elif self.shot_mode == 3:  # 逆時針
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
                radiusx = WIDTH / 2 - (self.rect.width / 2 + 10)
                radiusy = HEIGHT / 2 - (self.rect.height / 2 + 10)
                moved_time = time.time() - self.start_moved_time
                duration = 30
                if moved_time <= duration:
                    angle = -360 * (moved_time / duration) - 90
                    self.rect.centerx = WIDTH / 2 + math.cos(math.radians(angle)) * radiusx
                    self.rect.centery = HEIGHT / 2 + math.sin(math.radians(angle)) * radiusy
                else:
                    self.rect.center = (self.positionx, self.positiony)
        elif self.moved_mode == 4:
            if self.shot_mode == 1:
                self.positionx, self.positiony = (WIDTH / 2, HEIGHT / 2)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height / 2 + 10)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (WIDTH / 2, HEIGHT - (self.rect.height + 10))  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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
                self.positionx, self.positiony = (WIDTH / 2, self.rect.height + 10)  # 特別定位
                if self.rect.center != (self.positionx, self.positiony):  # 定位x和y
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

        if self.lives < self.original_lives / 6 and (self.image_index < len(self.images) - 1):  # 生命值降到 1/6 就切換圖檔
            x = self.rect.centerx
            y = self.rect.centery

            self.image_index += 1
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            self.mask = pygame.mask.from_surface(self.image)

        # 死亡時撥放動畫
        if self.lives <= 0:
            self.image = self.ani[self.ani_index]
            now = pygame.time.get_ticks()
            if not self.ani_timer:
                self.ani_timer = now
            if now - self.ani_timer >= 20:  # 約 0.01 秒切換一次圖檔
                self.ani_timer = now
                if self.ani_index < len(self.ani) - 1:
                    self.ani_index += 1
                    self.image = self.ani[self.ani_index]
                    if self.ani_index == len(self.ani) - 1:
                        self.round_shoot = True

    def shoot(self, player):
        global level, win_game
        speed = 3
        damage = 1
        if self.moved_mode == 1:
            if self.shot_mode == 1:
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
                if start_shot_time - self.last_shot_time >= 200:  # 控制每隔0.2秒發射一次
                    if shot_time < duration:
                        angle = radian * (shot_time / duration)
                        if self.initial_angle == 90 - radian / 2:
                            dx = speed * math.cos(math.radians(self.initial_angle + angle))
                            dy = speed * math.sin(math.radians(self.initial_angle + angle))
                        elif self.initial_angle == 90 + radian / 2:
                            dx = speed * math.cos(math.radians(self.initial_angle - angle))
                            dy = speed * math.sin(math.radians(self.initial_angle - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time >= duration:
                        if self.initial_angle == 90 - radian / 2:
                            self.initial_angle += radian
                        elif self.initial_angle == 90 + radian / 2:
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
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time < duration:
                        for angle in range(30, 150 + 1, 30):  # 5個角度
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
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time < duration:
                        for angle in range(270, 360 + 1, 30):  # 4個角度
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
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time < duration:
                        for angle in range(180, 270 + 1, 30):  # 4個角度
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
                    if start_shot_time - self.last_shot_time >= 300:
                        for angle in range(30, 150 + 1, 40):  # 4個角度
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
                if start_shot_time - self.last_shot_time >= 300:
                    if self.rect.centerx > self.positionx + self.frame:
                        for angle in range(200, 250 + 1, 25):  # 3個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.left, self.rect.top, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif self.rect.centerx < self.positionx - self.frame:
                        for angle in range(290, 340 + 1, 25):  # 3個角度
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
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time < duration:
                        for angle in range(0, 360, 45):  # 8個角度
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
                        if self.initial_angle == 90 - radian / 2:  # -90
                            dx = speed * math.cos(math.radians(self.initial_angle + angle))
                            dy = speed * math.sin(math.radians(self.initial_angle + angle))
                        elif self.initial_angle == 90 + radian / 2:  # 270
                            dx = speed * math.cos(math.radians(self.initial_angle - angle))
                            dy = speed * math.sin(math.radians(self.initial_angle - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time <= duration + 1:
                        None
                    else:
                        if self.initial_angle == 90 - radian / 2:
                            self.initial_angle += radian
                        elif self.initial_angle == 90 + radian / 2:
                            self.initial_angle -= radian
                        self.start_shot_time = time.time()
        elif self.moved_mode == 5:
            if self.shot_mode == 1 and self.rect.center == (self.positionx, self.positiony):
                duration = 8
                radian = 45
                delay_time = 3
                start_shot_time = pygame.time.get_ticks()
                shot_time = time.time() - self.start_shot_time
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time - delay_time < 0:  # 停滯
                        None
                    elif shot_time - delay_time < duration:
                        angle = radian * ((shot_time - delay_time) / duration)  # 右邊
                        dx = speed * math.cos(math.radians(self.initial_angle + radian - angle))
                        dy = speed * math.sin(math.radians(self.initial_angle + radian - angle))
                        barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                        all_sprites.add(barrage)
                        barrages.add(barrage)
                        angle = radian * ((shot_time - delay_time) / duration)  # 左邊
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
                if start_shot_time - self.last_shot_time >= 300:
                    if shot_time - delay_time < 0:
                        None
                    elif shot_time - delay_time < duration:
                        for angle in range(0, 180 + 1, 15):  # 12個角度
                            dx = math.cos(math.radians(angle)) * speed
                            dy = math.sin(math.radians(angle)) * speed
                            barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                            all_sprites.add(barrage)
                            barrages.add(barrage)
                        self.last_shot_time = start_shot_time
                    elif shot_time - delay_time >= duration:
                        self.shot_mode = 1
                        self.start_shot_time = time.time()

        if self.round_shoot:
            for angle in range(0, 360, 30):  # 12個
                dx = math.cos(math.radians(angle)) * speed
                dy = math.sin(math.radians(angle)) * speed
                barrage = Barrage(self.rect.centerx, self.rect.bottom, dx, dy, damage)
                all_sprites.add(barrage)
                barrages.add(barrage)
            if level < 5:
                level += 1
            else:
                win_game = True
            self.kill()


class Barrage(Sprite):
    def __init__(self, x, y, dx, dy, damage):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(barrage_img, (20, 30))
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


class Block(Sprite):
    def __init__(self, circle=None):
        Sprite.__init__(self)
        global level
        # 每個 level 的障礙物都不太一樣
        if level == 1:  # level 1 障礙物只會往下掉
            dice = random.randrange(0, 4)
            self.type = 1
            self.image = pygame.transform.scale(block_img[dice], (100, 60))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()  # 賦予定位的框架，rect 可以用來定位

            self.rect.bottom = random.randrange(-5, 0)
            position1 = random.randrange(40, int(WIDTH/2 - 50))
            position2 = random.randrange(int(WIDTH/2 + 50), int(WIDTH - 40))
            self.rect.centerx = random.choice([position1, position2])
            self.speed_x = 0
            self.speed_y = 1.2
        if level == 2:  # level 2 障礙物只會左右動
            self.type = 2
            self.image = pygame.transform.scale(block_img[4], (150, 70))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()

            self.rect.bottom = random.randrange(120, int(HEIGHT*(2/3)))
            dice = random.randrange(0, 2)
            if dice == 0:
                self.pointing = 0
                self.rect.centerx = 0 - self.rect.width
                self.speed_x = random.randrange(2, 5)
                self.speed_y = 0
            elif dice == 1:
                self.pointing = 1
                self.rect.centerx = WIDTH + self.rect.width
                self.speed_x = random.randrange(-4, -1)
                self.speed_y = 0
        if level == 3:   # 轉圈的物件
            self.type = 3
            self.image = pygame.transform.scale(block_img[5], (50, 50))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.radius = 300  # 圓弧半徑

            if circle == 1:
                self.center_big_circle = (-30, 160)
            if circle == 2:
                self.center_big_circle = (WIDTH+30, 160)
            if circle == 3:
                self.center_big_circle = (-30, HEIGHT/3)
            if circle == 4:
                self.center_big_circle = (WIDTH+30, HEIGHT/3)
            if circle == 5:
                self.center_big_circle = (-30, HEIGHT/4)
            if circle == 6:
                self.center_big_circle = (WIDTH+30, HEIGHT/4)

            self.external_point = (self.center_big_circle[0], self.center_big_circle[1] + self.radius)  # 外部點為圓心右側半徑處
            self.rect.center = self.external_point

            if circle % 2 != 0:  # 基數順時針轉
                self.angle = -90  # 從大圓的正上方開始繞大圓
                self.angular_speed = math.radians(10)
                self.prev_time = pygame.time.get_ticks()  # 儲存上一次的時間
                self.pointing = 0
            if circle % 2 == 0:  # 偶數逆時針轉
                self.angle = -90
                self.angular_speed = -math.radians(10)
                self.prev_time = pygame.time.get_ticks()  # 儲存上一次的時間
                self.pointing = 1

        if level == 4:
            self.type = 4

            dice = random.randrange(0, 2)
            if dice == 0:
                self.pointing = 0  # 代表向右
                self.image = pygame.transform.rotate(pygame.transform.scale(block_img[6], (400, 250)), -90)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.right = 0
                self.rect.top = random.randrange(50, int(HEIGHT/2) - 80)

                self.speed_x = 2
                self.speed_y = 2
            if dice == 1:
                self.pointing = 1  # 代表向左
                self.image = pygame.transform.rotate(pygame.transform.scale(block_img[6], (400, 220)), 90)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.left = WIDTH
                self.rect.top = random.randrange(70, int(HEIGHT / 2) - 80)

                self.speed_x = -2
                self.speed_y = 2

        if level == 5:
            self.type = 5
            self.image = pygame.transform.scale(block_img[6], (500, 420))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.top = HEIGHT
            self.rect.centerx = random.randrange(150, WIDTH - 150)

            dice = random.randrange(0, 2)

            if dice == 0:
                self.speed_x = 2
                self.speed_y = -2
            if dice == 1:
                self.speed_x = -2
                self.speed_y = -2

        self.lives = self.type + 5
        self.ani = [pygame.transform.scale(i, (self.rect.width, self.rect.height)) for i in explosion_img]
        self.ani_index = 0
        self.ani_timer = None

    def update(self, *args):
        if self.type == 1:
            self.rect.bottom += self.speed_y
            self.rect.centerx += self.speed_x

            if self.rect.top > HEIGHT + 20:
                self.kill()

        if self.type == 2:
            self.rect.bottom += self.speed_y
            self.rect.centerx += self.speed_x

            if self.pointing == 0:
                if self.rect.left > WIDTH + 10:
                    self.kill()
            if self.pointing == 1:
                if self.rect.right < - 10:
                    self.kill()

        if self.type == 3:
            now = pygame.time.get_ticks()
            dt = now - self.prev_time  # 計算時間增量

            self.angle += self.angular_speed * (dt / 1000)   # 將時間增量轉換為秒

            # 計算新的位置
            x = self.center_big_circle[0] + self.radius * math.cos(math.radians(self.angle))
            y = self.center_big_circle[1] + self.radius * math.sin(math.radians(self.angle))
            self.external_point = (x, y)
            self.rect.center = self.external_point

            if self.pointing == 0 and self.rect.center[0] <= -50:
                self.kill()
            if self.pointing == 1 and self.rect.center[0] >= WIDTH + 50:
                self.kill()

        if self.type == 4:
            self.rect.bottom += self.speed_y
            self.rect.centerx += self.speed_x

            if self.pointing == 0:
                if self.rect.left >= -20:
                    self.speed_x = -2
                if self.rect.right < -20:
                    self.kill()
            if self.pointing == 1:
                if self.rect.right <= WIDTH + 20:
                    self.speed_x = 2
                if self.rect.left > WIDTH + 20:
                    self.kill()

        if self.type == 5:
            self.rect.bottom += self.speed_y
            self.rect.centerx += self.speed_x

            if self.rect.top < HEIGHT-150:
                self.speed_y = 2

            if self.rect.top > HEIGHT + 30:
                self.kill()

        if self.lives <= 0:
            self.image = self.ani[self.ani_index]
            now = pygame.time.get_ticks()
            if not self.ani_timer:
                self.ani_timer = now
            if now - self.ani_timer >= 10:  # 約 0.01 秒切換一次圖檔
                self.ani_timer = now
                if self.ani_index < len(self.ani) - 1:
                    self.ani_index += 1
                    self.image = self.ani[self.ani_index]
                    if self.ani_index == len(self.ani) - 1:
                        enemy_explosion_sound.play()
                        dice = random.randrange(0, 3 + player.lives)  # 玩家的 lives 越少，越容易掉道具
                        if dice == 0:
                            new_item(enemy=bl)
                        self.kill()


class Item(Sprite):
    def __init__(self, enemy=None):
        Sprite.__init__(self)
        global level
        if level == 1:
            self.type = random.randrange(1, 3)  # type 對應 items 串列的 index
        if level == 2:
            self.type = random.randrange(1, 5)
        if level == 3:
            self.type = random.randrange(1, 7)
        if level >= 4:
            self.type = random.randrange(1, 9)

        self.image = items_img[self.type-1]

        # 用來做碰撞判斷的 mask 屬性
        self.mask = pygame.mask.from_surface(self.image)

        if enemy is not None:
            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = enemy.rect.centerx
            self.rect.bottom = enemy.rect.bottom
        else:
            self.rect = self.image.get_rect()  # rect 可以用來定位
            self.rect.centerx = random.randrange(50, WIDTH-50)
            self.rect.bottom = random.randrange(-40, 0)

        # 道具的墜落速度
        self.speed_y = 2
        self.speed_x = random.choice([-3, -2, 2, 3])

    def update(self, *args):
        self.rect.bottom += self.speed_y
        self.rect.centerx += self.speed_x

        # 一旦跑出畫面外，就要被移除
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()


def draw_lines_animation():
    global line_y, line_number, line_frame_count
    if line_frame_count >= 30:  # 約每 30 個 frame 切換一次直線的間隔
        surface_for_lines.fill((0, 0, 0, 0))  # 給 surface_for_lines 填充「透明色」，消除之前的直線
        if line_number == 1:
            line_number = 1.1
        else:
            line_number = 1
        line_frame_count = 0

    while line_y < HEIGHT:
        pygame.draw.line(surface_for_lines, LINES_COLOR, (0, line_y), (WIDTH, line_y), LINE_WIDTH)
        line_gap = INITIAL_LINE_GAP + line_y // (line_number * 4)  # 每次迴圈都增加直線的間隔
        line_y += line_gap
    if line_y >= HEIGHT:
        line_y = 0
    screen.blit(surface_for_lines, (0, 0))


def draw_init():
    global screen, line_frame_count, bgm
    img_title = init_title
    img_title_rect = img_title.get_rect()
    img_title_rect.centerx = WIDTH / 2
    img_title_rect.top = 150

    img_message = init_message
    img_message_rect = img_message.get_rect()
    img_message_rect.centerx = WIDTH / 2
    img_message_rect.top = 0

    bgm = intro_bgm

    waiting = True
    message_start_timer = pygame.time.get_ticks()

    while waiting:
        clock.tick(FPS)  # 控制 FPS，穩定單位時間內顯示的次數

        bgm_for_ui()

        screen.fill(BACKGROUND_COLOR)  # 給 screen 填滿顏色

        line_frame_count += 1
        draw_lines_animation()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - message_start_timer

        if 500 < elapsed_time < 1000:
            screen.blit(init_message, img_message_rect)

        if elapsed_time >= 1000:
            message_start_timer = pygame.time.get_ticks()

        screen.blit(init_title, img_title_rect)

        pygame.display.update()

        # 取得輸入
        for event in pygame.event.get():  # event.get() 會回傳現在發生的所有事件(包括滑鼠滑到哪、按下某按鍵等)
            if event.type == pygame.QUIT:
                sys.exit()  # 直接結束「程式運作」
            if event.type == pygame.KEYDOWN:  # 若 get() 回傳某按鍵「被按下」然後「被鬆開」, 就會讓 waiting 為 False
                waiting = False


def draw_pause():  # 遊戲迴圈內偵測到使用者按下 p 鍵，就會繪製 pause UI
    global paused, show_init
    screen.blit(pause_img, (110, 120))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)

        bgm_for_ui()

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
    global show_init
    screen.blit(dead_img, (110, 120))
    pygame.display.update()
    waiting = True

    while waiting:
        clock.tick(FPS)

        bgm_for_ui()

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

                    blocks.empty()

                    items.empty()
                    waiting = False
                    # del player_group, small_enemies, middle_enemies, big_enemies, bullets, barrages, items


def draw_note():  # 用來繪製給使用者的提醒和操作教學
    global screen, line_frame_count, play_note

    if play_note:
        img_note = note_img.copy()
        img_note_rect = img_note.get_rect()  # 沒有繼承 Sprite 就沒有 rect 屬性，只能用這種的
        img_note_rect.centerx = WIDTH / 2
        img_note_rect.top = 0

        fade_out_duration = 1000  # 淡出效果持續時間
        max_alpha = 255  # 最大透明度(不透明)

        waiting_note = True
        note_start_timer = pygame.time.get_ticks()

        while waiting_note:
            clock.tick(FPS)  # 控制 FPS，穩定單位時間內顯示的次數

            screen.fill(BACKGROUND_COLOR)  # 給 screen 填滿顏色

            line_frame_count += 1
            draw_lines_animation()

            now = pygame.time.get_ticks()
            elapsed_time = now - note_start_timer

            if elapsed_time < 5000:
                screen.blit(img_note, img_note_rect)
                pygame.display.update()
            if elapsed_time >= 5000:
                if (elapsed_time - 5000) < fade_out_duration:
                    alpha = int((1 - (elapsed_time - 5000) / fade_out_duration) * max_alpha)
                    img_note.set_alpha(alpha)  # 調整 note_img 圖檔的透明度，給 note_img 做出「淡出」效果
                    screen.blit(img_note, img_note_rect)
                    pygame.display.update()

                else:
                    waiting_note = False
            # 取得事件
            for event in pygame.event.get():  # event.get() 會回傳現在發生的所有事件(包括滑鼠滑到哪、按下某按鍵等)
                if event.type == pygame.QUIT:
                    sys.exit()  # 直接結束「程式運作」


def draw_tutorial():  # 播放遊戲教學
    global screen, line_frame_count, bgm, bgm_volume, play_tutorial

    if play_tutorial:
        fade_in_duration = 1000  # 淡入效果持續時間
        fade_out_duration = 1000  # 淡出效果持續時間
        max_alpha = 255  # 最大透明度(不透明)

        bgm = intro_bgm
        # 檢查音檔是否撥放完畢
        if not pygame.mixer.music.get_busy():
            # 重新載入音檔並加入串列
            pygame.mixer.music.load(bgm)
            pygame.mixer.music.play()

        img_tutorial = tutorial_img.copy()
        img_tutorial_rect = img_tutorial.get_rect()  # 沒有繼承 Sprite 就沒有 rect 屬性，只能用這種的
        img_tutorial_rect.centerx = WIDTH / 2
        img_tutorial_rect.top = 0

        waiting_tutorial = True
        tutorial_start_timer = pygame.time.get_ticks()

        while waiting_tutorial:
            clock.tick(FPS)  # 控制 FPS，穩定單位時間內顯示的次數

            screen.fill(BACKGROUND_COLOR)  # 給 screen 填滿顏色

            line_frame_count += 1
            draw_lines_animation()

            now = pygame.time.get_ticks()
            elapsed_time = now - tutorial_start_timer

            if elapsed_time < 4000:
                if elapsed_time < fade_in_duration:
                    alpha = int((elapsed_time / fade_in_duration) * max_alpha)
                    img_tutorial.set_alpha(alpha)  # 調整 note_img 圖檔的透明度，給 note_img 做出「淡入」效果
                    screen.blit(img_tutorial, img_tutorial_rect)
                    pygame.display.update()
                else:
                    screen.blit(img_tutorial, img_tutorial_rect)
                    pygame.display.update()
            if elapsed_time >= 4000:
                if (elapsed_time - 4000) < fade_out_duration:
                    alpha = int((1 - (elapsed_time - 4000) / fade_out_duration) * max_alpha)
                    img_tutorial.set_alpha(alpha)  # 調整 note_img 圖檔的透明度，給 note_img 做出「淡出」效果
                    screen.blit(img_tutorial, img_tutorial_rect)
                    pygame.display.update()
                else:
                    waiting_tutorial = False
            # 取得事件
            for event in pygame.event.get():  # event.get() 會回傳現在發生的所有事件(包括滑鼠滑到哪、按下某按鍵等)
                if event.type == pygame.QUIT:
                    sys.exit()  # 直接結束「程式運作」


def draw_level(surf):  # 繪製當前 level
    global level_numbers, level
    img = level_numbers[level-1]
    img_rect = img.get_rect()
    img_rect.centerx = WIDTH / 2
    img_rect.top = 30
    surf.blit(img, img_rect)


def draw_player_lives(surf, player):
    if player.lives > 0:
        img = player_lives_images[player.lives]
    elif player.lives <= 0:
        img = player_lives_images[0]
    img_rect = img.get_rect()
    img_rect.centerx = player.rect.centerx + 1
    img_rect.centery = player.rect.centery + 10
    surf.blit(img, img_rect)


def draw_enemy_lives(enemy):  # 這函式應該要寫在下面的 更新遊戲 部分，且大概是要放在 update() 底下
    for e in enemy:  # 遍歷敵機當前群組中的所有敵機
        bar_length = e.rect.width
        bar_height = 5
        fill = bar_length * (e.lives / e.original_lives)
        outline_rect = pygame.Rect(e.rect.left, e.rect.bottom + 5, bar_length, bar_height)
        fill = pygame.Rect(e.rect.left, e.rect.bottom + 5, fill, bar_height)
        pygame.draw.rect(screen, RED, outline_rect, 1)  # 最後一個參數可以設定此矩形的像素，設定成 1 的話就會畫出矩形細線
        pygame.draw.rect(screen, RED, fill)


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


def block_check():
    global level, block_timer

    if level == 1:
        if len(blocks) < 3 and time.time() - block_timer >= 3:
            new_block()
            block_timer = time.time()
    if level == 2:
        if len(blocks) < 1 and time.time() - block_timer >= 3:
            new_block()
            block_timer = time.time()
    if level == 3:
        dice = random.randrange(1, 7)
        if len(blocks) < 4 and time.time() - block_timer >= 2:
            new_block(dice=dice)
            block_timer = time.time()
    if level == 4 and len(blocks) < 3:
        new_block()
    if level == 5:
        if len(big_enemies) == 0 and len(blocks) < 2:
            new_block()
        elif len(big_enemies) > 0 and len(blocks) < 1:
            new_block()


def new_block(dice=None):
    global level

    if level != 3:
        block = Block()
        all_sprites.add(block)
        blocks.add(block)
    else:
        block = Block(circle=dice)
        all_sprites.add(block)
        blocks.add(block)


def new_item(enemy=None):  # 打死中型敵機掉道具
    if enemy is not None:
        i = Item(enemy)
        all_sprites.add(i)
        items.add(i)
    else:
        i = Item()
        all_sprites.add(i)
        items.add(i)


def check_collision(sprite1, sprite2):  # 用來判斷 sprite 物件之間是否有碰撞
    offset_x = sprite2.rect.x - sprite1.rect.x  # 用來校準 mask 碰撞判斷的定位
    offset_y = sprite2.rect.y - sprite1.rect.y
    result = sprite1.mask.overlap(sprite2.mask, (offset_x, offset_y))
    return result is not None  # 若 result 不為空就回傳 result


def play_bgm():
    global bgm, music_end_event, play_music, dead, bgm_volume

    if not bgm:
        bgm = normal_bgm_without_middle
    else:
        if play_music:
            if not big_enemies:
                if not middle_enemies:
                    bgm = normal_bgm_without_middle
                else:
                    bgm = normal_bgm_with_middle
            else:
                for b in big_enemies:
                    if b.lives >= 60 * level * (2 / 3):
                        bgm = boss_bgm_stage_1
                    elif b.lives >= 60 * level * (1 / 3):
                        bgm = boss_bgm_stage_2
                    elif b.lives < 60 * level * (1 / 3):
                        bgm = boss_bgm_stage_3
            if dead:
                bgm = bgm

        if play_music:
            pygame.mixer.music.load(bgm)
            pygame.mixer.music.set_volume(bgm_volume)
            pygame.mixer.music.play()

        if pygame.mixer.music.get_busy():
            play_music = False


def bgm_for_ui():
    global bgm, bgm_volume
    if not pygame.mixer.music.get_busy():
        # 重新載入音檔並加入串列
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.set_volume(bgm_volume)
        pygame.mixer.music.play()


def going_back():
    global screen, line_frame_count, bgm, bgm_volume, win_game, show_init

    img_end = ending_img.copy()
    img_end_rect = img_end.get_rect()  # 沒有繼承 Sprite 就沒有 rect 屬性，只能用這種的
    img_end_rect.centerx = WIDTH / 2
    img_end_rect.centery = HEIGHT / 2 - 30

    fade_in_duration = 1000  # 淡入效果持續時間
    fade_out_duration = 1000  # 淡出效果持續時間
    max_alpha = 255  # 最大透明度(不透明)

    bgm_for_ui()

    waiting_end = True
    end_start_timer = pygame.time.get_ticks()

    while waiting_end:
        clock.tick(FPS)  # 控制 FPS，穩定單位時間內顯示的次數

        screen.fill(BACKGROUND_COLOR)  # 給 screen 填滿顏色

        line_frame_count += 1
        draw_lines_animation()

        # 檢查音檔是否撥放完畢
        if not pygame.mixer.music.get_busy():
            # 重新載入音檔並加入串列
            pygame.mixer.music.load(bgm)
            pygame.mixer.music.play()

        now = pygame.time.get_ticks()
        elapsed_time = now - end_start_timer

        if elapsed_time < 4000:
            if elapsed_time < fade_in_duration:
                alpha = int((elapsed_time / fade_in_duration) * max_alpha)
                img_end.set_alpha(alpha)  # 調整 note_img 圖檔的透明度，給 note_img 做出「淡入」效果
                screen.blit(img_end, img_end_rect)
                pygame.display.update()
            else:
                screen.blit(img_end, img_end_rect)
                pygame.display.update()
        if elapsed_time >= 4000:
            if (elapsed_time - 4000) < fade_out_duration:
                alpha = int((1 - (elapsed_time - 4000) / fade_out_duration) * max_alpha)
                img_end.set_alpha(alpha)  # 調整 note_img 圖檔的透明度，給 note_img 做出「淡出」效果
                screen.blit(img_end, img_end_rect)
                pygame.display.update()
            else:
                bgm = intro_bgm
                pygame.mixer.music.load(bgm)
                pygame.mixer.music.play()
                waiting_end = False
                bgm = intro_bgm
                win_game = False
                show_init = True

        # 取得事件
        for event in pygame.event.get():  # event.get() 會回傳現在發生的所有事件(包括滑鼠滑到哪、按下某按鍵等)
            if event.type == pygame.QUIT:
                sys.exit()  # 直接結束「程式運作」


# 遊戲迴圈
running = True
show_init = True  # 之後要用來決定是否顯示起始畫面的變數
paused = False  # 玩家按下 p 鍵(暫定，但可以改)時，遊戲會暫停並顯示 pause UI
dead = False  # 玩家死掉時就會跳出輸掉的畫面
play_note = True  # 只有第一次才會撥放
play_tutorial = True

level = 1  # 用來改變關卡，同時此變數會改變敵機的生成方式

small_death = 0
middle_death = 0
middle_make = False  # 小型敵機死一定數量就會生成中型敵機
big_make = False  # 中型敵機死一定數量就會生成大型敵機
block_make = False  # 創建障礙物
item_make = False  # 從天上掉道具
win_game = False  # 打死 level 5 的大型敵機，使用者獲勝

block_timer = time.time()  # 用來計算每次創建障礙物中間隔了多少時間

bgm = None
play_music = True
music_end_event = pygame.USEREVENT + 1  # 用來判斷音檔是否撥放完畢的事件
pygame.mixer.music.set_endevent(music_end_event)

frame_counter = 0  # 每次遊戲循環給計數器加 1
collision_check_threshold = 3  # 設定成每 3 幀檢查一次碰撞，減少碰撞判斷的計算次數

async def main():
    global play_note, play_tutorial, play_music, running, show_init, all_sprites, small_enemies, middle_enemies, big_enemies, blocks, frame_counter, line_frame_count, bullets, barrages, bl, player_group, items, player, item_make, dead, paused, win_game

    while running:
        if show_init:  # 判斷是否顯示起始畫面
            draw_note()  # 提醒使用者要切換鍵盤語言
            draw_init()  # 先畫出起始 UI
            draw_tutorial() # 操作教學

            play_note = False
            play_tutorial = False

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
            blocks = pygame.sprite.Group()
            items = pygame.sprite.Group()

            show_init = False
            dead = False

            player = Player()
            all_sprites.add(player)
            player_group.add(player)

            pygame.mixer.music.stop()

            new_small(level)  # 每次遊戲的最開始都會有一個小型敵機出現

        clock.tick(FPS)  # 固定 FPS 控制畫面的切換
        # 到這裡為止都算遊戲的初始化

        # ******取得輸入******
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # 切換 pause 狀態
            if event.type == music_end_event:
                play_music = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

        # ******更新遊戲******
        play_bgm()

        for small_enemy in small_enemies:
            small_enemy.shoot()

        for middle_enemy in middle_enemies:
            middle_enemy.shoot(player)

        for big_enemy in big_enemies:
            big_enemy.shoot(player)

        if not show_init and not dead and paused:  # 判斷是否顯示暫停畫面
            draw_pause()  # 暫停 UI

        if player.lives <= 0:  # 玩家生命值低於零
            player.kill()
            dead = True

        if not show_init and dead:  # 判斷玩家是否死亡
            draw_dead()

        if not win_game:
            if len(small_enemies) < (level if level <= 2 else 2):  # 限制畫面中小型敵機的生成數量
                for i in range(0, random.randrange(1, 3), 1):
                    new_small(level)
            if len(small_enemies) >= 3 or big_enemies:
                if len(items) <= 1:
                    item_make = True
            block_check()

            if middle_make:
                new_middle(level)
                middle_make = False
            if big_make:
                new_big()
                big_make = False
            if item_make:
                new_item()
                item_make = False

        if win_game and not paused and not dead:  # 打死 level 5 大型敵機，使用者獲勝，遊戲結束
            screen.fill(BACKGROUND_COLOR)

            draw_lines_animation()

            for i in middle_enemies:
                i.lives = 0
            for i in small_enemies:
                i.lives = 0
            for i in blocks:
                i.lives = 0
            for i in bullets:
                i.kill()
            for i in barrages:
                i.kill()
            for i in items:
                i.kill()
            if player.rect.bottom < 0:
                if len(all_sprites) <= 1:
                    player.kill()
                    all_sprites.update()
                    all_sprites.draw(screen)
                    pygame.display.update()
                    going_back()
            if player_group:
                all_sprites.update(player)
            else:
                all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.update()

        if not paused and not dead and not win_game:  # dead、pause 或 win_game 就會停止更新遊戲
            all_sprites.update(player)
            frame_counter += 1

            if frame_counter >= collision_check_threshold:  # 限制碰撞判斷的計算次數
                for b in bullets:
                    for bl in blocks:
                        if check_collision(b, bl):
                            if type(b) == SpecialBullet and b.type in [6, 7]:
                                bl.lives -= 3
                            else:
                                bl.lives -= 1
                                b.play_ani = True

                for b in bullets:
                    for s in small_enemies:
                        if check_collision(b, s):  # 若 b 和 s 發生碰撞
                            if type(b) == SpecialBullet and b.type in [6, 7]:  # 「環狀」和「大絕招」
                                if not s.hit:
                                    if type(s) == SmallEnemy:
                                        s.lives -= 3
                                        s.hit = True
                            else:
                                b.play_ani = True
                                if type(s) == SmallEnemy:
                                    s.lives -= 1
                                    s.hit = True
                            if s.lives <= 0:
                                enemy_explosion_sound.play()
                                small_death += 1
                                if small_death >= (5 + level):  # 打死大於 5 + level 的小型敵機就會生成中型敵機
                                    if len(middle_enemies) < (level if level <= 2 else 2) and not big_enemies:  # 每關同時間最多只會有 level 架中型敵機
                                        middle_make = True

                for b in bullets:
                    for m in middle_enemies:
                        if check_collision(b, m):  # 若 b 和 m 發生碰撞
                            if type(b) == SpecialBullet and b.type in [6, 7]:  # 「環狀」和「大絕招」
                                if not m.hit:
                                    if type(m) == MiddleEnemy:
                                        m.lives -= 3
                                        m.hit = True
                            else:
                                b.play_ani = True
                                if type(m) == MiddleEnemy:
                                    m.lives -= 1
                                    m.hit = True
                            if m.lives <= 0:
                                m.shoot(player)
                                enemy_explosion_sound.play()
                                middle_death += 1
                                dice = random.randrange(0, 2 + player.lives)  # 玩家的 lives 越少，越容易掉道具
                                if dice == 0:
                                    new_item(enemy=m)
                                if middle_death >= (4 + level):  # 打死大於 4 + level 的中型敵機就會生成大型敵機
                                    if len(big_enemies) == 0:
                                        big_make = True
                                        middle_death = 0

                for b in bullets:
                    for be in big_enemies:
                        if check_collision(b, be):  # 若 b 和 be 發生碰撞
                            if type(b) == SpecialBullet and b.type in [6, 7]:  # 「環狀」和「大絕招」
                                if not be.hit:
                                    if type(be) == BigEnemy:
                                        be.lives -= 3
                                        be.hit = True
                            else:
                                b.play_ani = True
                                enemy_explosion_sound.play()
                                if type(be) == BigEnemy:
                                    be.lives -= 1
                            if be.lives <= 0:
                                be.shoot(player)

                if player.can_hit:
                    for p in player_group:
                        for s in small_enemies:
                            if check_collision(p, s):  # 若 p 和 s 發生碰撞
                                player.lives -= 1
                                if type(s) == SmallEnemy:
                                    s.lives -= 3
                                    player.can_hit = False

                                if s.lives <= 0:  # 當小型敵機的 lives 屬性數值歸零，將該小型敵機從群組中移除
                                    enemy_explosion_sound.play()
                                    small_death += 1
                                    if small_death >= (5 + level):  # 打死大於 5 + level 的小型敵機就會生成中型敵機
                                        if len(middle_enemies) < (level if level <= 2 else 2) and not big_enemies:  # 每關同時間最多只會有 level 架中型敵機
                                            middle_make = True

                    for p in player_group:
                        for m in middle_enemies:
                            if check_collision(p, m):  # 若 p 和 m 發生碰撞
                                player.lives -= 1
                                if type(m) == MiddleEnemy:
                                    m.lives -= 3
                                    player.can_hit = False
                                    m.hit = True

                                if m.lives <= 0:
                                    enemy_explosion_sound.play()
                                    middle_death += 1
                                    dice = random.randrange(0, 2 + player.lives)  # 玩家的 lives 越少，越容易掉道具
                                    if dice == 1:
                                        new_item(enemy=m)
                                    if middle_death >= (4 + level):  # 打死大於 4 + level 的中型敵機就會生成大型敵機
                                        if len(big_enemies) == 0:
                                            big_make = True
                                            middle_death = 0

                    for p in player_group:
                        for b in big_enemies:
                            if check_collision(p, b):  # 若 p 和 b 發生碰撞
                                player.lives -= 1
                                if type(b) == BigEnemy:
                                    b.lives -= 3
                                    player.can_hit = False
                                if b.lives <= 0:
                                    enemy_explosion_sound.play()

                    for p in player_group:
                        for br in barrages:
                            if check_collision(p, br):  # 若 p 和 br 發生碰撞
                                player.lives -= 1
                                player.can_hit = False
                                br.kill()

                    for p in player_group:
                        for b in blocks:
                            if check_collision(p, b):
                                enemy_explosion_sound.play()
                                b.lives -= 1
                                player.can_hit = False
                                player.lives -= 1
                # player.can_hit 的條件判斷到此為止
                for p in player_group:
                    for i in items:
                        if check_collision(p, i):  # 若 p 和 i 發生碰撞
                            i.kill()
                            item_get_sound.play()
                            if i.type == 1 and player.lives + 1 <= 3:
                                player.lives += 1
                            elif i.type == 3:
                                player.speed_up()
                            elif i.type in [2, 4, 5, 6, 7, 8]:
                                player.gun_up(i.type)

                frame_counter = 0  # 檢查碰撞判斷後就重置計數器

            # ******畫面顯示******
            screen.fill(BACKGROUND_COLOR)  # 給 screen 填滿顏色

            line_frame_count += 1
            draw_lines_animation()

            all_sprites.draw(screen)  # 指定畫在 screen 平面上

            if small_enemies:  # 畫出敵機的 lives
                draw_enemy_lives(small_enemies)
            if middle_enemies:
                draw_enemy_lives(middle_enemies)
            if big_enemies:
                draw_enemy_lives(big_enemies)

            for b in bullets:
                if type(b) == SpecialBullet and b.type in [6, 7]:
                    b.update(player)

            draw_player_lives(screen, player)
            draw_level(screen)  # 顯示當前關卡

            pygame.display.update()
    pygame.quit()
    await asyncio.sleep(0)
asyncio.run(main())

