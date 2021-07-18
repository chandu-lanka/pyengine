import pygame, sys, time, random
from pygame.locals import *
import imgs
import globals
import tile_logic
import map_loader
import tile_loader
import animations
import jumper_obj
import data.engine as e

# Basic Setup
pygame.init()
pygame.font.init()
pygame.mixer.pre_init()

WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300,200))
pygame.display.set_caption("game")

clock = pygame.time.Clock()
last_time = time.time()

# variables
moving_right = False
moving_left = False
width = 5
height = 14
player_rect = pygame.Rect(50, 50, width, height)
player_y_momentum = 0
air_timer = 0
game_map = map_loader.load_map('data/Maps/map')
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
jumper_objects = []
enemies = []
#e.load_animations('data/images/entities/')

font = pygame.font.SysFont('m5x7',16)

# for i in range(5):
#     enemies.append([0,e.entity(random.randint(0, 600) - 300,80,13,13, 'idle')])

for i in range(10):
    jumper_objects.append(jumper_obj.jumper_object((random.randint(0, 600)-300, 80)))

# Music & SFX
jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
jump_sound.set_volume(0.4)

animation_database = {}
animation_database['run'] = animations.load_animations('data/images/entities/Player/run', [4,4,4,4])
animation_database['idle'] = animations.load_animations('data/images/entities/Player/idle', [4,4,4])
animation_database['jump'] = animations.load_animations('data/images/entities/Player/jump', [1])
animation_database['fall'] = animations.load_animations('data/images/entities/Player/fall', [1])

player_action = 'idle'
player_frame = 0
player_flipped = False

while True:
    display.fill((116, 185, 255))
    font_render = font.render(f"FPS: {int(clock.get_fps())}", 1, (255, 255, 255))
    display.blit(font_render, (0,0))

    globals.true_scroll[0] += (player_rect.x - globals.true_scroll[0]-152)/20
    globals.true_scroll[1] += (player_rect.y - globals.true_scroll[1]-107)/20

    pygame.draw.rect(display, (7, 80, 50), pygame.Rect(0, 120, 300, 80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-globals.true_scroll[0]*background_object[0],background_object[1][1]-globals.true_scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150),obj_rect)
        else:
            pygame.draw.rect(display, (9,91,85),obj_rect)


    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            tile_loader.render_tiles(display, tile, x, y)
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player_y_momentum
    player_y_momentum += 1
    if player_y_momentum > 8:
        player_y_momentum = 8

    if player_movement[0] > 0:
        player_action, player_frame = animations.change_animation(player_action, player_frame, 'run')
        player_flipped = False

    if player_movement[0] == 0:
        player_action,player_frame = animations.change_animation(player_action,player_frame, 'idle')

    if player_movement[0] < 0:
        player_action, player_frame = animations.change_animation(player_action, player_frame, 'run')
        player_flipped = True

    player_rect, collisions = tile_logic.move(player_rect, player_movement, tile_loader.tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum = 0

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]

    player = animations.animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player, player_flipped, False),(player_rect.x-globals.true_scroll[0],player_rect.y-globals.true_scroll[1]))

    for jumper in jumper_objects:
        jumper.render(display, globals.true_scroll)
        if jumper.collision_test(player_rect):
            player_y_momentum = -15

    # for enemy in enemies:
    #     enemy[0] += 0.2
    #     enemy_movement = [0,enemy[0]]
    #     if enemy[0] > 3:
    #         enemy[0] = 3
    #     if player.x > enemy[1].x +  5:
    #         enemy_movement[0] = 1
    #     if player.x < enemy[1].x - 5:
    #         enemy_movement[0] = -1
    #     collision_types = enemy[1].move(enemy_movement, tile_loader.tile_rects)
    #     if collision_types['bottom'] == True:
    #         enemy[0] = 0
    #     enemy[1].display(display,globals.true_scroll)

        # if player_rect.colliderect(enemy[1].obj.rect):
        #     vertical_y_momentum = -4


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    player_y_momentum += -11
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(30)
