import pygame
import sys
import random
import time


# 初始化Pygame
pygame.init()
screen_width = 1400
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('天使之路')


# 分数位置和字体设置
f = pygame.font.Font('C:\\Windows\\Fonts\\simfang.ttf', 35)
score = 0
score_real = 0
text_background_color = (200, 229, 179)
text_foreground_color = (41, 39, 39)
textRect = pygame.Rect(580, 10, 150, 40)


# 生命值设置
lives = 3   # 默认三条命
life_text = f.render(f"生命值：{lives}", True, text_foreground_color, text_background_color)
life_text_rect = pygame.Rect(10, 10, 150, 40)


# 警告信息设置
warning_message = ''
warning_start_time = 0
warning_duration = 1000  # 警告信息显示时间


# 背景图设置
background_image = pygame.image.load('back_picture1.jpg')
background_rect = background_image.get_rect()
background_speed = 6  # 初始滚动速度
background_x_pos = 0
running = True
clock = pygame.time.Clock()
frame_counter = 0
speed_increase_interval = 240  # 每240帧增加一次速度


# 剧情故事
story_lines = [
    '那一天我重生了....',
    '我重生在闪动结算的前一个月。',
    '这一次我发誓要夺回我的校园跑。',
    '并在天使之路上躲避小白鹭冰淇淋。',
    '请选择你的角色！'
]

# 选择人物
character_images = [
    pygame.image.load('character1.png').convert_alpha(),
    pygame.image.load('character2.png').convert_alpha(),
]
target_size = (250, 400) 
for i in range(len(character_images)):
    character_images[i] = pygame.transform.scale(character_images[i], target_size)
for img in character_images:
    img.set_colorkey((255, 255, 255))
character_positions = [(300, 300), (850, 300)]  #角色位置
selected_character_index = None  #选择的角色索引

# 加载人物图片
characters = [[
    pygame.image.load('role11.png').convert_alpha(),
    pygame.image.load('role13.png').convert_alpha(),
    pygame.image.load('role12.png').convert_alpha()],#女生
    [
        pygame.image.load('role21.png').convert_alpha(),
        pygame.image.load('role23.png').convert_alpha(),
        pygame.image.load('role22.png').convert_alpha()]#男生
    
]

# 标记是否为举伞人物
is_showing_umbrella_character = False
# 加载举伞人物图片
umbrella_characters = [[
    pygame.image.load('role1_1.png').convert_alpha(),
    pygame.image.load('role1_3.png').convert_alpha(),
    pygame.image.load('role1_2.png').convert_alpha()],
    [pygame.image.load('role2_1.png').convert_alpha(),
    pygame.image.load('role2_3.png').convert_alpha(),
    pygame.image.load('role2_2.png').convert_alpha()
        ]
]


# 加载小白鹭图片
bird_image = pygame.image.load('bird.png').convert_alpha()
bird_rect = bird_image.get_rect()
bird_rect.topright = (1350, 50)  

# 加载并缩放护盾碎片图片
shield_piece_image = pygame.image.load('shield_piece.png').convert_alpha()
desired_shield_piece_size = (180,180)  # 设置护盾碎片大小
shield_piece_image = pygame.transform.scale(shield_piece_image, desired_shield_piece_size)
shield_pieces = []  # 存储护盾碎片的位置
next_shield_piece_time = time.time() + random.uniform(10, 20)  # 下一个护盾碎片出现的时间
shield_count = 0  # 玩家收集的护盾碎片数量

# 记录小白鹭静止
bird_still = False
bird_still_time = 0

# 加载障碍物图片
barrier_image = pygame.image.load('barrier1.png').convert_alpha()
barrier2_image = pygame.image.load('barrier2.png').convert_alpha()

# 加载背景音乐
pygame.mixer.music.load('BGM.mp3')
pygame.mixer.music.play(loops=-1)  # 循环播放
pygame.mixer.music.set_volume(0.5)

# 跳跃参数
jump_params = {
    'normal': {'jump_height': 200, 'velocity': -15, 'gravity': 0.55},
    'umbrella': {'jump_height': 250, 'velocity': -13.5, 'gravity': 0.4}
}

# 跳跃实现
jumping = False
jumping_started = False
umbrella_jumping = False
is_umbrella_used_in_jump = False

# 障碍物出现时间
last_barrier_time = time.time()
next_barrier_time = last_barrier_time + random.uniform(1, 3)  # 下一个障碍物生成的时间
barriers = []

# 鼠标左键
mouse_click_time = None
show_umbrella_duration = 1000 

# 游戏结束标志
game_over = False

def begin_screen():
    title_font = pygame.font.Font('C:\\Windows\\Fonts\\simfang.ttf', 60)
    button_font = pygame.font.Font('C:\\Windows\\Fonts\\simfang.ttf', 40)
    title_text = title_font.render('天使之路', True, text_foreground_color, text_background_color)
    button_text = button_font.render('开始游戏', True, text_foreground_color, text_background_color)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    button_rect = button_text.get_rect(center=(screen_width // 2, screen_height * 3 // 4))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    running = False  # 点击按钮后退出开始界面

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制标题和按钮
        screen.blit(title_text, title_rect)
        screen.blit(button_text, button_rect)

        pygame.display.flip()
        
def begin_story_screen():
    title_font = pygame.font.Font('C:\\Windows\\Fonts\\simfang.ttf', 60)
    current_line_index = 0
    running = True
    show_next_line = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_line_index < len(story_lines) - 1:
                    show_next_line = True
                else:
                    running = False  # 所有剧情播放完毕，退出开始界面

        if show_next_line:
            # 清除屏幕
            screen.blit(background_image, (0, 0))
            
            # 渲染当前剧情行
            title_text = title_font.render(story_lines[current_line_index], True, text_foreground_color, text_background_color)
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(title_text, title_rect)
            # 更新剧情索引
            current_line_index += 1
            show_next_line = False

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制当前剧情行
        if current_line_index < len(story_lines):
            title_text = title_font.render(story_lines[current_line_index], True, text_foreground_color, text_background_color)
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(title_text, title_rect)

        # 更新屏幕
        pygame.display.flip()
     
# 选择角色页面
def select_character_screen():
    global selected_character_index
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, pos in enumerate(character_positions):
                    rect = character_images[i].get_rect(topleft=pos)
                    if rect.collidepoint(mouse_pos):
                        selected_character_index = i
                        running = False  # 选择角色后退出选择页面

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制角色图像
        for i, pos in enumerate(character_positions):
            screen.blit(character_images[i], pos)

        # 更新屏幕
        pygame.display.flip()
        
# 游戏结束的界面运行
def show_game_over_screen():
    global game_over, score, score_real, lives, barriers, background_x_pos, frame_counter, background_speed
    global character_rect, umbrella_character_rect, bird_rect, last_barrier_time, next_barrier_time, jumping
    global jumping_started, umbrella_jumping, is_umbrella_used_in_jump, mouse_click_time, bird_still, bird_still_time
    global bird_has_dropped_barrier

    game_over_font = pygame.font.Font('C:\\Windows\\Fonts\\simfang.ttf', 50)
    game_over_text = game_over_font.render("游戏结束！", True, text_foreground_color, text_background_color)
    game_over_text_rect = game_over_text.get_rect(center=(700, 250))
    
    restart_text = game_over_font.render("按R键重新开始", True, text_foreground_color, text_background_color)
    restart_text_rect = restart_text.get_rect(center=(700, 350))

    quit_text = game_over_font.render("按Q键退出游戏", True, text_foreground_color, text_background_color)
    quit_text_rect = quit_text.get_rect(center=(700, 450))

    while game_over:
        screen.fill(text_background_color)
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(restart_text, restart_text_rect)
        screen.blit(quit_text, quit_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按下R键重新开始游戏
                    # 重置游戏状态
                    score = 0
                    score_real = 0
                    lives = 3
                    barriers.clear()
                    background_x_pos = 0
                    frame_counter = 0
                    background_speed = 6
                    character_rect.bottomleft = (85, 700)
                    umbrella_character_rect.bottomleft = (85, 700)
                    bird_rect.topright = (1350, 50)
                    last_barrier_time = time.time()
                    next_barrier_time = last_barrier_time + random.uniform(1, 3)
                    jumping = False
                    jumping_started = False
                    umbrella_jumping = False
                    is_umbrella_used_in_jump = False
                    mouse_click_time = None
                    bird_still = False
                    bird_still_time = 0
                    bird_has_dropped_barrier = False
                    game_over = False  # 结束游戏结束界面
                elif event.key == pygame.K_q:  # 按下Q键退出游戏
                    pygame.quit()
                    sys.exit()
          
def manage_shield_pieces(screen, character_rect, umbrella_character_rect, background_speed):
    global shield_pieces, next_shield_piece_time, shield_count, lives

    # 生成新的护盾碎片
    current_time = time.time()
    if current_time >= next_shield_piece_time:
        new_shield_piece = shield_piece_image.get_rect()
        new_shield_piece.bottomright = (1400, random.randint(400,600))  # 随机高度
        shield_pieces.append(new_shield_piece)
        next_shield_piece_time = current_time + random.uniform(5, 10)  # 设置下一次生成时间

    # 更新并绘制所有护盾碎片
    for piece in shield_pieces[:]:
        piece.x -= background_speed
        screen.blit(shield_piece_image, piece)

        # 检测玩家是否收集到护盾碎片
        collected = False
        if not jumping or umbrella_jumping:
            if character_rect.colliderect(piece):
                collected = True
        else:
            if umbrella_character_rect.colliderect(piece):
                collected = True

        if collected:
            shield_count += 1
            shield_pieces.remove(piece)
            if shield_count >= 3:  # 收集满3个碎片
                shield_count = 0  # 重置计数
                lives += 1  # 生命值+1
# 游戏主程序
begin_screen()
begin_story_screen()
select_character_screen()
character_rect = characters[selected_character_index][0].get_rect()
character_rect.bottomleft = (85, 700)
current_character_index = 0
character_switch_counter = 0
character_switch_interval = 10  # 每8帧切换一次
bird_has_dropped_barrier = False  # 用于标记小白鹭是否掉落过障碍物
umbrella_character_rect = umbrella_characters[selected_character_index][0].get_rect()
umbrella_character_rect.bottomleft = (85, 700)  # 统一位置
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:  # 按下空格键开始跳跃
                jump_type = 'normal'
                if mouse_click_time is not None:  # 如果正在举伞，则使用举伞跳跃参数
                    jump_type = 'umbrella'
                    umbrella_jumping = True

                velocity = jump_params[jump_type]['velocity']
                gravity = jump_params[jump_type]['gravity']
                jumping = True
                jumping_started = True  # 开始跳跃

                if current_character_index == 1:
                    current_character_index = (current_character_index + 1) % len(characters)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 检测鼠标左键点击
            mouse_click_time = pygame.time.get_ticks()
            if jumping:
                is_umbrella_used_in_jump = True
                warning_message = "危险！你在跳不能撑伞！"
                warning_start_time = pygame.time.get_ticks()  # 记录警告信息开始显示的时间

    if not game_over:
        background_x_pos -= background_speed
        if background_x_pos <= -background_rect.width:
            background_x_pos = 0

        frame_counter += 1
        if frame_counter >= speed_increase_interval:
            background_speed += 0.15  # 每次增加0.15的速度
            frame_counter = 0

        screen.blit(background_image, (background_x_pos, 0))  # 实现背景图滚动的连接
        screen.blit(background_image, (background_x_pos + background_rect.width, 0))

        # 里程数显示
        if frame_counter % 8 == 0:
            score_real = score_real + 0.005
            score_real += (background_speed - 4) / 1000
            score = round(score_real, 2)  

        text = f.render(f"里程数：{score}km", True, text_foreground_color, text_background_color)
        screen.blit(text, textRect)

        # 更新角色位置
        if jumping:
            if umbrella_jumping:
                umbrella_character_rect.y += velocity
                velocity += gravity
                if umbrella_character_rect.bottom >= 700:  # 触地检测
                    umbrella_character_rect.bottom = 700
                    jumping = False
                    jumping_started = False  
                    umbrella_jumping = False  
                    is_umbrella_used_in_jump = False  
            else:
                character_rect.y += velocity
                velocity += gravity
                if character_rect.bottom >= 700:  # 触地检测
                    character_rect.bottom = 700
                    jumping = False
                    jumping_started = False  

        # 实现人物贴图交替显示
        if not jumping_started:  
            character_switch_counter += 1  
            if character_switch_counter >= character_switch_interval:  
                current_character_index = (current_character_index + 1) % len(characters)  
                character_switch_counter = 0  

        # 检查是否需要显示举伞图片
        if mouse_click_time is not None and not is_umbrella_used_in_jump:  
            current_time = pygame.time.get_ticks()
            if umbrella_jumping or (current_time - mouse_click_time < show_umbrella_duration):
                is_showing_umbrella_character = True
                current_umbrella_index = current_character_index
                screen.blit(umbrella_characters[selected_character_index][current_umbrella_index], umbrella_character_rect)
            else:
                mouse_click_time = None
                is_showing_umbrella_character = False 
                screen.blit(characters[selected_character_index][current_character_index], character_rect)
        else:
            is_showing_umbrella_character = False 
            screen.blit(characters[selected_character_index][current_character_index], character_rect)  # 默认显示不举伞的人物

        # 显示警告信息
        if warning_message and pygame.time.get_ticks() - warning_start_time < warning_duration:
            warning_text = f.render(warning_message, True, (255, 0, 0), text_background_color)
            screen.blit(warning_text, (500, 200) )
        elif warning_message:
            warning_message = '' 
            is_umbrella_used_in_jump = False  

        # 绘制小白鹭图片部分的修改
        if not bird_still:
            bird_rect.x -= background_speed  
            if bird_rect.right < 0:  
                bird_rect.topright = (1350, 50)  
                bird_still = True
                bird_still_time = random.randint(2, 8)  
                bird_has_dropped_barrier = False  # 重置标志
        else:
            bird_still_time -= 1 / 60  
            if bird_still_time <= 0:
                bird_still = False

        # 检查小白鹭位置，若在指定位置且没有生成过障碍物，则生成
        if 106 <= bird_rect.left < 114 and bird_rect.top == 50 and not bird_has_dropped_barrier:
            new_barrier2_rect = barrier2_image.get_rect()
            new_barrier2_rect.topleft = (180, 160)  
            barriers.append(new_barrier2_rect)  
            bird_still_time = 60  
            bird_has_dropped_barrier = True  # 设置标志，防止再次生成

        screen.blit(bird_image, bird_rect)
        manage_shield_pieces(screen, character_rect, umbrella_character_rect, background_speed)
        current_time = time.time()

        # 生成新的障碍物
        if current_time >= next_barrier_time:
            new_barrier_rect = barrier_image.get_rect()
            new_barrier_rect.bottomright = (1400, 700)  
            barriers.append(new_barrier_rect)
            next_barrier_time = current_time + random.uniform(1.5, 4)

        # 绘制所有障碍物
        for barrier_rect in barriers[:]:
            is_barrier2 = barrier_rect.height == barrier2_image.get_height()

            if is_barrier2:  # barrier2 的碰撞检测
                barrier_rect.y += 8  
                if barrier_rect.top > 750:  
                    barriers.remove(barrier_rect)  
            else:
                barrier_rect.x -= background_speed  
                if barrier_rect.right < 0: 
                    barriers.remove(barrier_rect)  
            screen.blit(barrier_image if barrier_rect.height != barrier2_image.get_height() else barrier2_image, barrier_rect)  # 绘制障碍物

        # 碰撞检测
        for barrier_rect in barriers[:]:
            is_barrier2 = barrier_rect.height == barrier2_image.get_height()

            if is_barrier2:  # barrier2 的碰撞检测
                if warning_message:  
                        continue  #有bug警告则跳过判定
            
                if is_showing_umbrella_character:  
                    if umbrella_character_rect.colliderect(barrier_rect):  
                        barriers.remove(barrier_rect)  
                else: 
                    if character_rect.colliderect(barrier_rect):  
                        barriers.remove(barrier_rect)  
                        lives -= 1  
                        if lives <= 0:  
                            game_over = True

            else:  # barrier1 的碰撞检测
                if umbrella_jumping: 
                    if umbrella_character_rect.colliderect(barrier_rect): 
                        barriers.remove(barrier_rect) 
                else:  
                    if character_rect.colliderect(barrier_rect):  
                        barriers.remove(barrier_rect) 
                        lives -= 1  
                        if lives <= 0:  
                            game_over = True

        # 生命值显示
        life_text = f.render(f"生命值：{lives}", True, text_foreground_color, text_background_color)
        screen.blit(life_text, life_text_rect)

    else:
        show_game_over_screen()

    pygame.display.flip()
    clock.tick(60)